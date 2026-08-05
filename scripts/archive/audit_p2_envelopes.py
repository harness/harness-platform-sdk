#!/usr/bin/env python
"""
P2 Envelope Audit: Inspect OpenAPI spec to verify envelope shapes for P2 domains.

Extracts request/response schemas for Services, Roles, Resource Groups, and
Role Assignments from the OpenAPI spec to confirm or correct their envelope
declarations (flat vs named-wrapper).

Script approach only — all findings reproducible by re-running.
Saved to scripts/ for traceability; not wired into mise.toml.
"""

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
        return response_obj  # ref target missing — return original
    return resolved


def resolve_schema_ref(spec: Dict[str, Any], schema: Any) -> Any:
    """Resolve top-level $ref in schema."""
    if isinstance(schema, dict) and '$ref' in schema:
        ref_path = schema['$ref']
        if ref_path.startswith('#/components/schemas/'):
            schema_name = ref_path.split('/')[-1]
            return spec['components']['schemas'].get(schema_name, schema)
    return schema


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


def build_tag_domain_map(spec: Dict[str, Any]) -> Dict[str, str]:
    """Build inverted map from operation-level tag → canonical domain key."""
    tag_map = {}
    for group in spec.get('x-tagGroups', []):
        group_name = group.get('name', '')
        domain_key = group_name.lower().replace(' ', '_').replace('-', '_')
        for tag in group.get('tags', []):
            tag_map[tag] = domain_key
    return tag_map


def get_operations_for_domain(
    spec: Dict[str, Any],
    target_domain: str,
    tag_domain_map: Dict[str, str]
) -> List[Tuple[str, str, Dict[str, Any]]]:
    """
    Find all operations for a given domain.

    Args:
        spec: OpenAPI spec
        target_domain: Domain key to search for (e.g., "services")
        tag_domain_map: Inverted tag→domain map

    Returns:
        List of (path, method, operation) tuples
    """
    operations = []
    paths = spec.get('paths', {})

    for path, path_item in paths.items():
        for method in ['get', 'post', 'put', 'patch', 'delete']:
            if method not in path_item:
                continue

            operation = path_item[method]
            # Check if any operation tag matches target domain
            for tag in operation.get('tags', []):
                if tag_domain_map.get(tag) == target_domain:
                    operations.append((path, method, operation))
                    break

    return operations


def is_object_schema(spec: Dict[str, Any], schema: Any) -> bool:
    """
    Check if a schema represents a domain object wrapper (not metadata or peer fields).

    Returns True if:
    - Schema is a direct `$ref` to a domain-like schema name (not utility names like
      Scope, Metadata, etc.), OR
    - Schema is `type: object` with named properties AND looks like domain data

    Returns False for scalars, arrays, generic metadata objects, or utility schemas.

    Args:
        spec: OpenAPI spec for resolving $refs
        schema: Schema dict to check

    Returns:
        bool: True if schema is a domain object wrapper
    """
    if not isinstance(schema, dict):
        return False

    # Check if this is a `$ref` to a utility/metadata schema (not a domain)
    if '$ref' in schema:
        ref_name = schema['$ref'].split('/')[-1]
        # Filter out known utility schemas
        utility_schemas = {
            'AuthzScope', 'RoleScope', 'Scope', 'AuthzValidationResult',
            'AuthzGovernanceMetadata', 'Metadata', 'Error',
            'ResponseDTO', 'PageResponse'
        }
        if any(util in ref_name for util in utility_schemas):
            return False
        # Utility schemas or helpers don't end in "Response" if they're in responses
        # But a wrapped domain schema should be like "OrganizationResponse", "ServiceResponse"
        # Simple heuristic: if it's a $ref and NOT a utility, it's a domain object
        return True

    # After resolution, check for type and properties
    resolved = resolve_schema_ref(spec, schema)

    if not isinstance(resolved, dict):
        return False

    # `type: object` with explicit properties is a domain object
    # (bare `type: object` without properties is just a generic dict/metadata)
    if resolved.get('type') == 'object' and 'properties' in resolved:
        return True

    return False


def extract_list_envelope(spec: Dict[str, Any], operations: List[Tuple[str, str, Dict[str, Any]]]) -> Dict[str, Any]:
    """Extract list endpoint response schema and determine unwrap_field."""
    for path, method, operation in operations:
        # List operations are typically GET with no {id} segment
        if method.lower() != 'get' or '{' in path.split('/')[-1]:
            continue

        if 'responses' not in operation:
            continue

        responses = operation['responses']
        for status_code in ('200', '201'):
            if status_code in responses:
                resp = resolve_response_ref(spec, responses[status_code])
                if 'content' in resp:
                    content = resp['content'].get('application/json', {})
                    schema = content.get('schema')
                    if schema:
                        schema = resolve_schema_ref(spec, schema)
                        schema = strip_metadata(schema)

                        # Detect if this is an array or wrapped
                        result_type = schema.get('type')
                        items_schema = schema.get('items', {})

                        if result_type == 'array':
                            # Direct array response
                            unwrap_field = None
                            return {
                                'path': path,
                                'method': method,
                                'schema': schema,
                                'unwrap_field': unwrap_field,
                                'type': 'direct_array'
                            }
                        elif items_schema.get('type') == 'object':
                            # Wrapped in object with items field
                            properties = items_schema.get('properties', {})
                            if 'data' in properties:
                                data_schema = properties['data']
                                data_schema = resolve_schema_ref(spec, data_schema)
                                if data_schema.get('type') == 'array':
                                    # Standard wrapper: {"data": [...]}
                                    unwrap_field = None
                                    return {
                                        'path': path,
                                        'method': method,
                                        'schema': schema,
                                        'unwrap_field': unwrap_field,
                                        'type': 'wrapped_data'
                                    }
                            # Check for single-item wrappers like {"services": [...]}
                            for key, prop in properties.items():
                                if key not in ('status', 'message', 'code', 'data'):
                                    prop = resolve_schema_ref(spec, prop)
                                    if prop.get('type') == 'array':
                                        # Found wrapper key
                                        return {
                                            'path': path,
                                            'method': method,
                                            'schema': schema,
                                            'unwrap_field': key,
                                            'type': 'wrapped_named'
                                        }

    return {}


def extract_singleton_envelope(spec: Dict[str, Any], operations: List[Tuple[str, str, Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Extract get/create/update response schema and determine unwrap_field.

    Uses structural object-type detection:
    - Count object-typed properties at top level (or within `data` if present)
    - Exactly 1 object + scalar siblings → wrapped_named
    - All scalars → flat
    - Multiple objects or unresolvable → ambiguous
    """
    metadata_fields = {
        'status', 'message', 'code', 'created', 'updated',
        'createdAt', 'lastModifiedAt', 'createdDate', 'lastModifiedDate',
        'data', 'created_at', 'last_modified_at'
    }

    for path, method, operation in operations:
        # Singleton operations: GET with {id}, POST/PUT
        if method.lower() == 'get' and '{' not in path.split('/')[-1]:
            continue

        if 'responses' not in operation:
            continue

        responses = operation['responses']
        for status_code in ('200', '201'):
            if status_code in responses:
                resp = resolve_response_ref(spec, responses[status_code])
                if 'content' in resp:
                    content = resp['content'].get('application/json', {})
                    schema = content.get('schema')
                    if schema:
                        schema = resolve_schema_ref(spec, schema)
                        schema = strip_metadata(schema)
                        properties = schema.get('properties', {})

                        # Determine what level to inspect for structure
                        # If response has "data", inspect inside; otherwise inspect top-level
                        if 'data' in properties:
                            # Unwrap one level to look inside "data"
                            data_schema = properties['data']
                            data_schema = resolve_schema_ref(spec, data_schema)
                            data_schema = strip_metadata(data_schema)
                            target_properties = data_schema.get('properties', {})
                        else:
                            # Inspect top-level directly
                            target_properties = properties

                        # Structural test: count object-typed properties
                        object_keys = []
                        scalar_keys = []

                        for key, prop in target_properties.items():
                            if key not in metadata_fields:
                                if is_object_schema(spec, prop):
                                    object_keys.append(key)
                                else:
                                    scalar_keys.append(key)

                        # Verdict based on structure
                        if len(object_keys) == 1:
                            # Exactly one object + optional scalar siblings → wrapped
                            return {
                                'path': path,
                                'method': method,
                                'schema': schema,
                                'unwrap_field': object_keys[0],
                                'type': 'wrapped_named'
                            }
                        elif len(object_keys) == 0:
                            # All scalars → flat
                            return {
                                'path': path,
                                'method': method,
                                'schema': schema,
                                'unwrap_field': None,
                                'type': 'flat'
                            }
                        else:
                            # Multiple objects → ambiguous
                            return {
                                'path': path,
                                'method': method,
                                'schema': schema,
                                'unwrap_field': None,
                                'type': 'ambiguous',
                                'reason': f'Multiple object-typed properties: {object_keys}'
                            }

    return {}


def extract_request_envelope(spec: Dict[str, Any], operations: List[Tuple[str, str, Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Extract create/update request body schema.

    Uses two-pass approach:
    - Pass 1: /v1/ paths only (modern SDK endpoints)
    - Pass 2: any path fallback (legacy endpoints)
    - If no requestBody found: return not_found sentinel

    Uses structural object-type detection:
    - Count top-level object-typed properties
    - Exactly 1 object + scalar siblings → wrapped_named
    - All scalars → flat
    - Multiple objects or unresolvable → ambiguous
    """
    metadata_fields = {
        'status', 'message', 'code', 'created', 'updated',
        'createdAt', 'lastModifiedAt', 'createdDate', 'lastModifiedDate'
    }

    def extract_from_operation(path: str, method: str, operation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Try to extract envelope from a single operation."""
        if 'requestBody' not in operation:
            return None

        rb = operation['requestBody']
        if 'content' not in rb:
            return None

        content = rb['content'].get('application/json', {})
        schema = content.get('schema')
        if not schema:
            return None

        schema = resolve_schema_ref(spec, schema)
        schema = strip_metadata(schema)
        properties = schema.get('properties', {})

        # Structural test: count object-typed top-level properties
        object_keys = []
        scalar_keys = []

        for key, prop in properties.items():
            if key not in metadata_fields:
                if is_object_schema(spec, prop):
                    object_keys.append(key)
                else:
                    scalar_keys.append(key)

        # Verdict based on structure
        if len(object_keys) == 1 and len(scalar_keys) >= 0:
            # Exactly one object + optional scalar siblings → wrapped
            return {
                'path': path,
                'method': method,
                'schema': schema,
                'wrapper_key': object_keys[0],
                'type': 'wrapped_named'
            }
        elif len(object_keys) == 0:
            # All scalars → flat
            return {
                'path': path,
                'method': method,
                'schema': schema,
                'wrapper_key': None,
                'type': 'flat'
            }
        else:
            # Multiple objects → ambiguous
            return {
                'path': path,
                'method': method,
                'schema': schema,
                'wrapper_key': None,
                'type': 'ambiguous',
                'reason': f'Multiple object-typed properties: {object_keys}'
            }

    # Pass 1: /v1/ paths only
    for path, method, operation in operations:
        if not path.startswith('/v1/'):
            continue
        if method.lower() not in ('post', 'put', 'patch'):
            continue

        result = extract_from_operation(path, method, operation)
        if result:
            return result

    # Pass 2: any path (fallback)
    for path, method, operation in operations:
        if method.lower() not in ('post', 'put', 'patch'):
            continue

        result = extract_from_operation(path, method, operation)
        if result:
            return result

    # No requestBody found on any matching operation
    return {'type': 'not_found', 'wrapper_key': None, 'path': None}


def audit_domain(
    spec: Dict[str, Any],
    domain: str,
    tag_domain_map: Dict[str, str]
) -> Dict[str, Any]:
    """Audit a single domain for envelope shape."""
    operations = get_operations_for_domain(spec, domain, tag_domain_map)

    if not operations:
        return {
            'domain': domain,
            'verdict': 'UNKNOWN',
            'reason': 'No operations found for domain'
        }

    list_env = extract_list_envelope(spec, operations)
    singleton_env = extract_singleton_envelope(spec, operations)
    request_env = extract_request_envelope(spec, operations)

    # Determine verdict
    list_unwrap = list_env.get('unwrap_field')
    singleton_unwrap = singleton_env.get('unwrap_field')
    request_wrapper = request_env.get('wrapper_key')

    # If any shows a wrapper, it's wrapped
    is_wrapped = any([
        list_unwrap is not None,
        singleton_unwrap is not None,
        request_wrapper is not None
    ])

    if is_wrapped:
        # All three should have the same wrapper key
        wrapper_key = singleton_unwrap or list_unwrap or request_wrapper
        verdict = 'CONFIRMED_WRAPPED'
        reason = f'Named wrapper: "{wrapper_key}"'
    else:
        verdict = 'CONFIRMED_FLAT'
        reason = 'No wrapper detected in any endpoint'

    return {
        'domain': domain,
        'verdict': verdict,
        'reason': reason,
        'list_envelope': list_env,
        'singleton_envelope': singleton_env,
        'request_envelope': request_env,
    }


def generate_audit_report(findings: Dict[str, Dict[str, Any]]) -> str:
    """Generate markdown report from audit findings."""
    report = """# P2 Envelope Audit Report

This report documents the envelope shapes (request/response wrappers) for P2 domains
as extracted from the OpenAPI spec via spec inspection.

## Findings Summary

"""

    # Summary table
    report += "| Domain | Verdict | Reason |\n"
    report += "|--------|---------|--------|\n"
    for domain in ['services', 'roles', 'resource_groups', 'role_assignments']:
        finding = findings.get(domain, {})
        verdict = finding.get('verdict', 'UNKNOWN')
        reason = finding.get('reason', '')
        report += f"| {domain} | {verdict} | {reason} |\n"

    report += "\n---\n\n"

    # Detailed findings per domain
    for domain in ['services', 'roles', 'resource_groups', 'role_assignments']:
        finding = findings.get(domain)
        if not finding:
            continue

        report += f"## {domain.upper()}\n\n"
        report += f"**Verdict:** {finding['verdict']}\n\n"
        report += f"**Evidence:** {finding['reason']}\n\n"

        # Envelope Contract table
        report += "### Envelope Contract\n\n"
        report += "| Property | Value |\n"
        report += "|----------|-------|\n"

        # Extract values from findings — each row from its own extractor only
        list_env = finding.get('list_envelope', {})
        singleton_env = finding.get('singleton_envelope', {})
        request_env = finding.get('request_envelope', {})

        list_unwrap = list_env.get('unwrap_field')
        singleton_unwrap = singleton_env.get('unwrap_field')
        request_wrapper = request_env.get('wrapper_key')
        request_type = request_env.get('type', 'not_found')

        # Render list envelope row (from list_env only)
        list_display = f"{list_env.get('type', 'not_found')} (unwrap: {list_unwrap})" \
            if list_env else "not_found"

        # Render singleton envelope row (from singleton_env only)
        singleton_display = f"{singleton_env.get('type', 'not_found')} (unwrap: {singleton_unwrap})" \
            if singleton_env else "not_found"

        # Render request body wrapper row — no fallback to singleton values
        # Check for SPEC_INCOMPLETE condition or contradiction
        if not request_env or request_type == 'not_found':
            request_display = "SPEC_INCOMPLETE — no requestBody found on /v1/ endpoints"
        elif request_type == 'flat' and finding.get('verdict') == 'CONFIRMED_WRAPPED':
            request_display = (
                "flat (wrapper: None) — NOTE: contradicts singleton finding; verify live"
            )
        else:
            request_display = f"{request_type} (wrapper: {request_wrapper})"

        # Render rows — each from its own extractor, no fallback chain
        report += f"| List envelope | {list_display} |\n"
        report += f"| Singleton envelope | {singleton_display} |\n"
        report += f"| Request body wrapper | {request_display} |\n"
        report += f"| unwrap_field (list) | {list_unwrap or 'None'} |\n"
        report += f"| unwrap_field (singleton) | {singleton_unwrap or 'None'} |\n"

        report += "\n"

    return report


def main():
    """Main entry point."""
    spec_path = Path('openapi/harness-openapi-normalized.yaml')

    if not spec_path.exists():
        logger.error("OpenAPI spec not found: %s", spec_path)
        return 1

    logger.info("Loading OpenAPI spec: %s", spec_path)
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)

    tag_domain_map = build_tag_domain_map(spec)

    # Target domains in scope
    domains = ['services', 'roles', 'resource_groups', 'role_assignments']
    findings = {}

    for domain in domains:
        logger.info("Auditing domain: %s", domain)
        result = audit_domain(spec, domain, tag_domain_map)
        findings[domain] = result

        # Print summary line
        verdict = result['verdict']
        reason = result['reason']
        print(f"[{verdict}] {domain} — {reason}")

    # Generate report
    report = generate_audit_report(findings)

    output_path = Path('docs/p2_envelope_audit.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    logger.info("Audit report written to: %s", output_path)

    # Exit 0 on success
    return 0


if __name__ == '__main__':
    sys.exit(main())
