# Copyright (c) 2026 Harness Solution Factory. All Rights Reserved.
#!/bin/python
"""
Permanent drift detection tooling for harness_python_sdk.

Extracts caller-facing schemas from Harness OpenAPI specs for all domains
via x-tagGroups, computes checksums at endpoint and domain granularity,
and detects drift against a baseline.

KNOWN GAPS (documented, not bugs):
  - components/requestBodies $ref pattern not handled — Harness does not
    currently use this; revisit if it appears in future spec versions.
  - $ref expansion is one level deep only — nested schema references are
    not recursively resolved.
"""

import argparse
import datetime
import hashlib
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def canonicalize(schema: Any) -> str:
    """
    Recursively strip metadata keys from schema and return canonical JSON.

    Strips: description, example, examples, and all x-* extension keys.
    """
    if isinstance(schema, dict):
        cleaned = {}
        for key, value in schema.items():
            # Skip metadata keys
            if key in ('description', 'example', 'examples') or key.startswith('x-'):
                continue
            cleaned[key] = canonicalize(value)
        return json.dumps(cleaned, sort_keys=True, separators=(',', ':'))
    elif isinstance(schema, list):
        return json.dumps([canonicalize(item) for item in schema],
                         sort_keys=True, separators=(',', ':'))
    else:
        return json.dumps(schema, separators=(',', ':'))


def strip_metadata(obj: Any) -> Any:
    """Recursively strip metadata keys from schema object."""
    if isinstance(obj, dict):
        return {
            k: strip_metadata(v)
            for k, v in obj.items()
            if k not in ('description', 'example', 'examples') and not k.startswith('x-')
        }
    elif isinstance(obj, list):
        return [strip_metadata(item) for item in obj]
    else:
        return obj


def resolve_response_ref(
    spec: dict,
    response_obj: dict,
) -> dict:
    """
    Resolve a response-level $ref to components/responses.

    Handles the two-level pattern:
      {'$ref': '#/components/responses/OrganizationResponse'}
      → spec['components']['responses']['OrganizationResponse']
      → {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/...}}}}

    Returns the resolved response object, or the original if not a components/responses ref.
    """
    if not isinstance(response_obj, dict):
        return response_obj
    ref = response_obj.get('$ref', '')
    if not ref.startswith('#/components/responses/'):
        return response_obj
    response_name = ref.split('/')[-1]
    resolved = spec.get('components', {}).get('responses', {}).get(response_name)
    if resolved is None:
        return response_obj  # ref target missing — return original, let existing logic handle
    return resolved


def resolve_schema_ref(spec: Dict[str, Any], schema: Any) -> Any:
    """Resolve top-level $ref in schema, handling both dict and string references."""
    if isinstance(schema, dict) and '$ref' in schema:
        ref_path = schema['$ref']
        if ref_path.startswith('#/components/schemas/'):
            schema_name = ref_path.split('/')[-1]
            return spec['components']['schemas'].get(schema_name, schema)
    return schema


def inline_one_level_refs(spec: Dict[str, Any], schema: Any) -> Any:
    """
    For each property value that is a $ref, resolve it one level deep.
    Do not recurse further.
    """
    if not isinstance(schema, dict):
        return schema

    result = {}
    for key, value in schema.items():
        if isinstance(value, dict):
            if '$ref' in value:
                # Resolve this reference one level
                ref_path = value['$ref']
                if ref_path.startswith('#/components/schemas/'):
                    schema_name = ref_path.split('/')[-1]
                    result[key] = spec['components']['schemas'].get(schema_name, value)
                else:
                    result[key] = value
            else:
                # Recurse into nested objects (but don't expand nested refs)
                result[key] = value
        else:
            result[key] = value

    return result


def extract_schemas_from_operation(
    spec: Dict[str, Any],
    operation: Dict[str, Any]
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract request and response schemas from an operation.

    Returns: (request_schema_json, response_schema_json)
    Both are canonicalized JSON strings, or None if not present.
    """
    request_schema = None
    response_schema = None

    # Extract request body schema (POST/PUT/PATCH only)
    if 'requestBody' in operation:
        rb = operation['requestBody']
        if 'content' in rb:
            # Prefer application/json
            for content_type in ('application/json', 'application/x-www-form-urlencoded'):
                if content_type in rb['content']:
                    schema = rb['content'][content_type].get('schema')
                    if schema:
                        schema = resolve_schema_ref(spec, schema)
                        schema = strip_metadata(schema)
                        schema = inline_one_level_refs(spec, schema)
                        request_schema = json.dumps(schema, sort_keys=True, separators=(',', ':'))
                        break

    # Extract 200/201 response schema
    if 'responses' in operation:
        responses = operation['responses']
        for status_code in ('200', '201'):
            if status_code in responses:
                resp = responses[status_code]
                resp = resolve_response_ref(spec, resp)  # Resolve components/responses refs first
                if 'content' in resp:
                    for content_type in ('application/json', 'application/x-www-form-urlencoded'):
                        if content_type in resp['content']:
                            schema = resp['content'][content_type].get('schema')
                            if schema:
                                schema = resolve_schema_ref(spec, schema)
                                schema = strip_metadata(schema)
                                schema = inline_one_level_refs(spec, schema)
                                response_schema = json.dumps(schema, sort_keys=True, separators=(',', ':'))
                                break
                if response_schema:
                    break

    return request_schema, response_schema


def build_tag_domain_map(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Build inverted map from operation-level tag → canonical domain key.

    Dynamically processes all x-tagGroups, normalizing group names:
    lowercase, spaces and hyphens → underscores.

    Args:
        spec: The OpenAPI spec dictionary

    Returns:
        Inverted map: {'Pipelines': 'pipelines', 'Input Sets': 'pipelines',
                       'Triggers': 'pipelines', 'Organization': 'organizations', ...}
    """
    tag_map = {}
    for group in spec.get('x-tagGroups', []):
        group_name = group.get('name', '')
        # Normalize group name: lowercase, spaces/hyphens → underscores
        domain_key = group_name.lower().replace(' ', '_').replace('-', '_')
        for tag in group.get('tags', []):
            tag_map[tag] = domain_key
    return tag_map


def get_domain_from_operation(
    operation: Dict[str, Any],
    path: str,
    tag_domain_map: Dict[str, str]
) -> Optional[str]:
    """
    Determine domain from operation tags or path prefix.

    Args:
        operation: The OpenAPI operation object
        path: The operation path
        tag_domain_map: Inverted map from operation tags to domain keys

    Returns:
        Domain key, or None if not determinable
    """
    # Check operation tags against the inverted map
    for tag in operation.get('tags', []):
        if tag in tag_domain_map:
            return tag_domain_map[tag]

    return None


def extract_endpoints(spec_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Extract all endpoints for all domains.

    Returns dict: {
        'domain1': {'operationId': {'endpoint': ..., 'request': ..., 'response': ...}},
        'domain2': {...}
    }
    """
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)

    # Build tag→domain map from x-tagGroups at load time
    tag_domain_map = build_tag_domain_map(spec)

    # Initialize endpoints_by_domain dict with all domains found
    endpoints_by_domain = {}
    identified_by_domain = {}

    for group in spec.get('x-tagGroups', []):
        group_name = group.get('name', '')
        domain_key = group_name.lower().replace(' ', '_').replace('-', '_')
        endpoints_by_domain[domain_key] = {}
        identified_by_domain[domain_key] = 0

    paths = spec.get('paths', {})
    for path, path_item in paths.items():
        for method in ['get', 'post', 'put', 'patch', 'delete']:
            if method not in path_item:
                continue

            operation = path_item[method]
            operation_id = operation.get('operationId')
            if not operation_id:
                continue

            domain = get_domain_from_operation(operation, path, tag_domain_map)
            if not domain:
                continue

            # Count all identified endpoints in this domain
            if domain in identified_by_domain:
                identified_by_domain[domain] += 1

            request_schema, response_schema = extract_schemas_from_operation(spec, operation)

            # Skip if no response schema found (only include caller-facing endpoints)
            if not response_schema:
                continue

            endpoints_by_domain[domain][operation_id] = {
                'path': path,
                'method': method.upper(),
                'request': request_schema,
                'response': response_schema
            }

    # Print endpoint counts by domain (identified before schema filtering)
    for domain in sorted(endpoints_by_domain.keys()):
        with_schemas = len(endpoints_by_domain[domain])
        identified = identified_by_domain.get(domain, 0)
        logger.info("%s: %d identified, %d with schemas", domain, identified, with_schemas)

    return endpoints_by_domain


def compute_checksums(endpoints_by_domain: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute checksums at both endpoint and domain granularity.

    Returns: {
        'per_endpoint': {'domain:operationId': '<sha256>'},
        'per_domain': {'domain': '<sha256>'}
    }
    """
    result = {
        'per_endpoint': {},
        'per_domain': {}
    }

    for domain, endpoints in endpoints_by_domain.items():
        domain_canonical_strings = []

        # Sort by operationId for deterministic ordering
        for op_id in sorted(endpoints.keys()):
            endpoint = endpoints[op_id]

            # Per-endpoint checksum
            request_str = endpoint['request'] or ''
            response_str = endpoint['response'] or ''
            combined = request_str + response_str

            endpoint_checksum = hashlib.sha256(combined.encode()).hexdigest()
            result['per_endpoint'][f"{domain}:{op_id}"] = endpoint_checksum

            # Accumulate for domain checksum
            domain_canonical_strings.append(combined)

        # Per-domain checksum
        domain_combined = ''.join(domain_canonical_strings)
        domain_checksum = hashlib.sha256(domain_combined.encode()).hexdigest()
        result['per_domain'][domain] = domain_checksum

    return result


def baseline_mode(spec_path: str, output_path: str) -> int:
    """Extract and checksum baseline spec, write results."""
    logger.info("Extracting endpoints from baseline spec: %s", spec_path)

    endpoints_by_domain = extract_endpoints(spec_path)

    checksums = compute_checksums(endpoints_by_domain)

    # Write baseline with today's ISO date
    baseline_data = {
        'spec_date': datetime.date.today().isoformat(),
        'per_endpoint': checksums['per_endpoint'],
        'per_domain': checksums['per_domain']
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(baseline_data, f, indent=2)

    logger.info("Baseline written to: %s", output_path)
    logger.info("Total endpoints indexed: %d", len(checksums['per_endpoint']))

    return 0


def compare_mode(baseline_path: str, comparison_spec: str) -> int:
    """Compare baseline against new spec, print results to stdout."""
    logger.info("Loading baseline from: %s", baseline_path)

    with open(baseline_path, 'r', encoding='utf-8') as f:
        baseline_data = json.load(f)

    logger.info("Extracting endpoints from comparison spec: %s", comparison_spec)
    endpoints_by_domain = extract_endpoints(comparison_spec)

    checksums = compute_checksums(endpoints_by_domain)

    baseline_endpoints = baseline_data['per_endpoint']
    comparison_endpoints = checksums['per_endpoint']

    # Endpoint-level diff
    all_op_ids = set(baseline_endpoints.keys()) | set(comparison_endpoints.keys())

    exit_code = 0
    for op_key in sorted(all_op_ids):
        baseline_cs = baseline_endpoints.get(op_key)
        comparison_cs = comparison_endpoints.get(op_key)

        if baseline_cs is None:
            status = 'ADDED'
            exit_code = 0  # ADDED is non-blocking
        elif comparison_cs is None:
            status = 'REMOVED'
            exit_code = 1  # REMOVED is blocking
        elif baseline_cs == comparison_cs:
            status = 'UNCHANGED'
        else:
            status = 'CHANGED'
            exit_code = 1  # CHANGED is blocking

        print(f"{op_key}: {status}")

    return exit_code


def main():
    parser = argparse.ArgumentParser(
        description="Drift detection for Harness Python SDK: extract schemas and compare against baseline"
    )
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare against baseline (requires baseline to exist)'
    )
    parser.add_argument(
        '--baseline-path',
        default='docs/model_checksums.json',
        help='Path to baseline checksums file'
    )

    args = parser.parse_args()

    spec_path = 'openapi/harness-openapi-normalized.yaml'

    if args.compare:
        if not Path(args.baseline_path).exists():
            logger.error("Baseline not found: %s. Run without --compare first.", args.baseline_path)
            return 1
        return compare_mode(args.baseline_path, spec_path)
    else:
        return baseline_mode(spec_path, args.baseline_path)


if __name__ == '__main__':
    sys.exit(main())
