#!/bin/python
# Copyright (c) 2026 Harness Solution Factory. All Rights Reserved.
"""
Pagination inventory regeneration tool for harness_python_sdk.

Re-scans the normalized OpenAPI spec and regenerates docs/pagination_inventory.md
with classification of all list endpoints as OFFSET, CURSOR, or UNKNOWN.

This script is idempotent: running it multiple times produces identical output.
"""

import datetime
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def build_tag_domain_map(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Build inverted map from operation-level tag → canonical domain key.

    Dynamically processes all x-tagGroups, normalizing group names:
    lowercase, spaces and hyphens → underscores.

    Args:
        spec: The OpenAPI spec dictionary

    Returns:
        Inverted map: {'Pipelines': 'pipelines', 'Input Sets': 'pipelines', ...}
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
    tag_domain_map: Dict[str, str]
) -> Optional[str]:
    """
    Determine domain from operation tags.

    Args:
        operation: The OpenAPI operation object
        tag_domain_map: Inverted map from operation tags to domain keys

    Returns:
        Domain key, or None if not determinable
    """
    # Check operation tags against the inverted map
    for tag in operation.get('tags', []):
        if tag in tag_domain_map:
            return tag_domain_map[tag]

    return None


def is_list_endpoint(operation: Dict[str, Any], operation_id: str, path: str) -> bool:
    """
    Determine if an operation is a list endpoint.

    Checks for:
    - operationId or path containing 'list', 'getAll', 'findAll'
    - Response schema is an array or contains pagination fields
    """
    operation_id_lower = operation_id.lower()
    path_lower = path.lower()

    # Check operationId and path for list indicators
    list_indicators = ['list', 'getall', 'findall', 'search']
    is_likely_list = any(ind in operation_id_lower or ind in path_lower for ind in list_indicators)

    if is_likely_list:
        return True

    # Check if response schema indicates a list (array type or has pagination fields)
    if 'responses' in operation:
        for status_code in ('200', '201'):
            if status_code in operation['responses']:
                resp = operation['responses'][status_code]
                # Handle response refs
                if isinstance(resp, dict) and '$ref' in resp:
                    continue  # Skip refs for now
                if isinstance(resp, dict) and 'content' in resp:
                    for content_type in resp['content']:
                        schema = resp['content'][content_type].get('schema', {})
                        if isinstance(schema, dict):
                            # Check if schema is an array
                            if schema.get('type') == 'array':
                                return True
                            # Check if schema contains pagination fields
                            if 'properties' in schema:
                                props = schema['properties']
                                pagination_fields = {
                                    'pageIndex', 'pageSize', 'totalItems',
                                    'page', 'size', 'limit',
                                    'nextPageToken', 'cursor'
                                }
                                if any(f in props for f in pagination_fields):
                                    return True

    return False


def classify_pagination_style(
    operation: Dict[str, Any],
    spec: Dict[str, Any]
) -> str:
    """
    Classify a list endpoint's pagination style.

    Classification rules (applied in order):
    1. Response schema contains nextPageToken, cursor → CURSOR
    2. Response schema contains pageIndex, pageSize, totalItems, page, size, limit → OFFSET
    3. Neither found → UNKNOWN

    Args:
        operation: The OpenAPI operation object
        spec: The full OpenAPI spec (for ref resolution)

    Returns:
        'OFFSET', 'CURSOR', or 'UNKNOWN'
    """
    if 'responses' not in operation:
        return 'UNKNOWN'

    for status_code in ('200', '201'):
        if status_code not in operation['responses']:
            continue

        resp = operation['responses'][status_code]

        # Handle response refs
        if isinstance(resp, dict) and '$ref' in resp:
            ref_path = resp['$ref']
            if ref_path.startswith('#/components/responses/'):
                response_name = ref_path.split('/')[-1]
                resp = spec.get('components', {}).get('responses', {}).get(response_name, {})

        if not isinstance(resp, dict) or 'content' not in resp:
            continue

        for content_type in resp['content']:
            schema = resp['content'][content_type].get('schema', {})
            if not isinstance(schema, dict):
                continue

            # Check for $ref and resolve one level
            if '$ref' in schema:
                ref_path = schema['$ref']
                if ref_path.startswith('#/components/schemas/'):
                    schema_name = ref_path.split('/')[-1]
                    schema = spec.get('components', {}).get('schemas', {}).get(schema_name, {})

            # For array responses, check the items schema
            if schema.get('type') == 'array':
                items_schema = schema.get('items', {})
                if isinstance(items_schema, dict):
                    # Check items for pagination fields
                    props = items_schema.get('properties', {})
                    if not props and '$ref' in items_schema:
                        ref_path = items_schema['$ref']
                        if ref_path.startswith('#/components/schemas/'):
                            schema_name = ref_path.split('/')[-1]
                            items_schema = spec.get('components', {}).get('schemas', {}).get(schema_name, {})
                            props = items_schema.get('properties', {})

            # Check for pagination fields in the main schema or items
            props = schema.get('properties', {})
            cursor_fields = {'nextPageToken', 'cursor', 'pageToken'}
            offset_fields = {'pageIndex', 'pageSize', 'totalItems', 'page', 'size', 'limit'}

            if any(f in props for f in cursor_fields):
                return 'CURSOR'
            if any(f in props for f in offset_fields):
                return 'OFFSET'

    return 'UNKNOWN'


def extract_list_endpoints(spec_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract all list endpoints from the spec, grouped by domain.

    Returns dict: {
        'domain1': [
            {'operationId': '...', 'path': '...', 'method': '...', 'style': 'OFFSET|CURSOR|UNKNOWN'}
        ],
        ...
    }
    """
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)

    tag_domain_map = build_tag_domain_map(spec)

    # Initialize endpoints_by_domain dict with all domains
    endpoints_by_domain = {}
    for group in spec.get('x-tagGroups', []):
        group_name = group.get('name', '')
        domain_key = group_name.lower().replace(' ', '_').replace('-', '_')
        endpoints_by_domain[domain_key] = []

    paths = spec.get('paths', {})
    for path, path_item in paths.items():
        for method in ['get', 'post', 'put', 'patch', 'delete']:
            if method not in path_item:
                continue

            operation = path_item[method]
            operation_id = operation.get('operationId')
            if not operation_id:
                continue

            # Check if this is a list endpoint
            if not is_list_endpoint(operation, operation_id, path):
                continue

            domain = get_domain_from_operation(operation, tag_domain_map)
            if not domain:
                continue

            # Classify pagination style
            style = classify_pagination_style(operation, spec)

            endpoints_by_domain[domain].append({
                'operationId': operation_id,
                'path': path,
                'method': method.upper(),
                'style': style
            })

    return endpoints_by_domain


def generate_pagination_md(endpoints_by_domain: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate the pagination inventory markdown document."""
    lines = []

    lines.append("# Pagination Inventory")
    lines.append("<!-- Generated by scripts/refresh_pagination.py. Do not edit manually. -->")
    lines.append(f"<!-- Last updated: {datetime.date.today().isoformat()} -->")
    lines.append("")

    # Build table rows, grouped by domain
    table_rows = []

    for domain in sorted(endpoints_by_domain.keys()):
        endpoints = endpoints_by_domain[domain]
        # Sort by operationId within each domain
        for endpoint in sorted(endpoints, key=lambda e: e['operationId']):
            table_rows.append({
                'domain': domain,
                'operationId': endpoint['operationId'],
                'path': endpoint['path'],
                'method': endpoint['method'],
                'style': endpoint['style'],
                'notes': ''  # Can be extended for future use
            })

    # Write table header
    lines.append("| Domain | OperationId | Path | Method | Pagination Style | Notes |")
    lines.append("|---|---|---|---|---|---|")

    # Write table rows
    for row in table_rows:
        lines.append(
            f"| {row['domain']} | {row['operationId']} | {row['path']} | {row['method']} | {row['style']} | {row['notes']} |"
        )

    lines.append("")

    return '\n'.join(lines)


def main():
    """Main entry point."""
    spec_path = 'openapi/harness-openapi-normalized.yaml'
    output_path = 'docs/pagination_inventory.md'

    logger.info("Scanning spec for list endpoints: %s", spec_path)
    endpoints_by_domain = extract_list_endpoints(spec_path)

    # Count statistics
    total_endpoints = sum(len(eps) for eps in endpoints_by_domain.values())
    offset_count = sum(sum(1 for e in eps if e['style'] == 'OFFSET') for eps in endpoints_by_domain.values())
    cursor_count = sum(sum(1 for e in eps if e['style'] == 'CURSOR') for eps in endpoints_by_domain.values())
    unknown_count = sum(sum(1 for e in eps if e['style'] == 'UNKNOWN') for eps in endpoints_by_domain.values())

    # Generate markdown
    markdown_output = generate_pagination_md(endpoints_by_domain)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_output)

    logger.info("Pagination inventory updated: %s", output_path)

    # Print summary
    print(f"Pagination inventory updated: {total_endpoints} endpoints classified — OFFSET={offset_count}, CURSOR={cursor_count}, UNKNOWN={unknown_count}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
