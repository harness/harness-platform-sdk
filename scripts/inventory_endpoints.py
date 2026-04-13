#!/bin/python
# Copyright (c) 2026 Harness Solution Factory. All Rights Reserved.
"""
P1 Endpoint Inventory Spike: Extract unimplemented endpoints from Pipelines, Connectors, Secrets.

Reads openapi/harness-openapi-normalized.yaml and generates docs/p1_endpoint_inventory.md
with a per-domain breakdown of:
  - Total endpoint count
  - Implemented methods (list, get, create, update, delete)
  - Unimplemented endpoints with operationId, method, path, and priority
  - Category classification (execution/trigger, validation, bulk, sub-resource, status/health, other)
  - Recommended priority (HIGH/MEDIUM/LOW)
"""

import datetime
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
        return response_obj
    return resolved


def has_response_schema(spec: Dict[str, Any], operation: Dict[str, Any]) -> bool:
    """
    Check if operation has a 200/201 response with a schema.

    Args:
        spec: The OpenAPI spec
        operation: The operation object

    Returns:
        True if operation has a response schema, False otherwise
    """
    if 'responses' not in operation:
        return False

    for status_code in ('200', '201'):
        if status_code not in operation['responses']:
            continue

        resp = operation['responses'][status_code]
        resp = resolve_response_ref(spec, resp)

        if isinstance(resp, dict) and 'content' in resp:
            for content_type in resp['content']:
                if 'schema' in resp['content'][content_type]:
                    return True

    return False


def classify_endpoint(
    operation_id: str,
    path: str,
    method: str
) -> Tuple[str, str]:
    """
    Classify an endpoint by category and assign priority.

    Categories:
      - execution/trigger: POST to execution/trigger endpoints
      - validation: POST/GET validation, test, validate endpoints
      - bulk: bulk/batch operations
      - sub-resource CRUD: CRUD on nested resources
      - status/health: status, health, monitor endpoints
      - other: everything else

    Priority:
      - HIGH: execution/trigger (POST), sub-resource CRUD (POST/PUT), bulk POST
      - MEDIUM: status/health, validation queries, sub-resource GET
      - LOW: bulk DELETE, other operations

    Args:
        operation_id: The operationId
        path: The endpoint path
        method: HTTP method

    Returns:
        (category, priority)
    """
    op_id_lower = operation_id.lower()
    path_lower = path.lower()

    # Execution/trigger
    if 'execute' in op_id_lower or 'trigger' in op_id_lower:
        if method == 'POST':
            return 'execution/trigger', 'HIGH'
        return 'execution/trigger', 'MEDIUM'

    # Validation
    if any(word in op_id_lower for word in ['validate', 'test', 'check']):
        if method == 'POST':
            return 'validation', 'HIGH'
        return 'validation', 'MEDIUM'

    # Bulk
    if 'bulk' in op_id_lower or 'batch' in op_id_lower:
        if method == 'POST':
            return 'bulk', 'HIGH'
        elif method == 'DELETE':
            return 'bulk', 'LOW'
        return 'bulk', 'MEDIUM'

    # Status/health
    if any(word in op_id_lower for word in ['status', 'health', 'monitor']):
        return 'status/health', 'MEDIUM'

    # Sub-resource CRUD detection (nested path patterns)
    # Look for patterns like /resource/{id}/sub-resource/{id2}
    path_segments = path.split('/')
    # Count segments with braces (path parameters)
    param_segments = [s for s in path_segments if '{' in s]
    if len(param_segments) >= 2:
        # Multiple parameters suggest nested/sub-resource
        if method in ('POST', 'PUT'):
            return 'sub-resource CRUD', 'HIGH'
        elif method == 'GET':
            return 'sub-resource CRUD', 'MEDIUM'
        elif method == 'DELETE':
            return 'sub-resource CRUD', 'LOW'

    # Default: other
    if method == 'POST':
        return 'other', 'MEDIUM'
    elif method in ('PUT', 'PATCH'):
        return 'other', 'MEDIUM'
    elif method == 'GET':
        return 'other', 'LOW'
    elif method == 'DELETE':
        return 'other', 'LOW'

    return 'other', 'MEDIUM'


def extract_endpoints(spec_path: str, target_domains: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Extract all endpoints for target domains from the spec.

    Returns dict: {
        'domain1': {'operationId': {'path': ..., 'method': ..., 'summary': ...}},
        'domain2': {...}
    }
    """
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)

    # Build tag→domain map from x-tagGroups at load time
    tag_domain_map = build_tag_domain_map(spec)

    # Initialize endpoints_by_domain dict for target domains only
    endpoints_by_domain = {domain: {} for domain in target_domains}

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
            if not domain or domain not in target_domains:
                continue

            # Only include if operation has a response schema (caller-facing)
            if not has_response_schema(spec, operation):
                continue

            summary = operation.get('summary', '')
            description = operation.get('description', '')

            endpoints_by_domain[domain][operation_id] = {
                'path': path,
                'method': method.upper(),
                'summary': summary,
                'description': description,
            }

    return endpoints_by_domain


def get_implemented_operation_ids(domain: str) -> Dict[str, str]:
    """
    Get the implemented operationIds for a domain from existing API files.

    Maps operationIds to their corresponding method names (list, get, create, update, delete).

    Returns: {'operationId': 'method_name', ...}
    """
    # Hardcoded mapping from existing P1 API implementations
    # Extracted by analyzing the API paths and endpoint operationIds

    implemented = {}

    if domain == 'pipelines':
        # From src/harness_python_sdk/api/pipelines.py
        # Endpoint: GET /v1/orgs/{org}/projects/{project}/pipelines → list-pipelines
        # Endpoint: GET /v1/orgs/{org}/projects/{project}/pipelines/{pipeline} → get-pipeline
        # Endpoint: POST /v1/orgs/{org}/projects/{project}/pipelines → create-pipeline
        # Endpoint: PUT /v1/orgs/{org}/projects/{project}/pipelines/{pipeline} → update-pipeline
        # Endpoint: DELETE /v1/orgs/{org}/projects/{project}/pipelines/{pipeline} → delete-pipeline
        implemented = {
            'list-pipelines': 'list',
            'get-pipeline': 'get',
            'create-pipeline': 'create',
            'update-pipeline': 'update',
            'delete-pipeline': 'delete',
        }
    elif domain == 'connectors':
        # From src/harness_python_sdk/api/connectors.py
        # Endpoint: GET /ng/api/connectors → getConnectorList
        # Endpoint: GET /ng/api/connectors/{identifier} → getConnector
        # Endpoint: POST /ng/api/connectors → createConnector
        # Endpoint: PUT /ng/api/connectors → updateConnector (ng/api doesn't have delete on base URL)
        # Endpoint: DELETE /ng/api/connectors/{identifier} → deleteConnector
        implemented = {
            'getConnectorList': 'list',
            'getConnector': 'get',
            'createConnector': 'create',
            'updateConnector': 'update',
            'deleteConnector': 'delete',
        }
    elif domain == 'secrets':
        # From src/harness_python_sdk/api/secrets.py
        # Endpoint: GET /ng/api/v2/secrets → listSecretsV2
        # Endpoint: GET /ng/api/v2/secrets/{identifier} → getSecretV2
        # Endpoint: POST /ng/api/v2/secrets → postSecret
        # Note: ng/api/v2/secrets doesn't have standard update/delete at root level
        # But v1 endpoints exist (not in current implementation)
        implemented = {
            'listSecretsV2': 'list',
            'getSecretV2': 'get',
            'postSecret': 'create',
            'deleteSecretV2': 'delete',
        }

    return implemented


def generate_inventory_md(
    endpoints_by_domain: Dict[str, Dict[str, Any]],
) -> str:
    """Generate the P1 endpoint inventory markdown document."""
    lines = []

    lines.append("# P1 Endpoint Inventory")
    lines.append("<!-- Generated by scripts/inventory_endpoints.py. Do not edit manually. -->")
    lines.append(f"<!-- Last updated: {datetime.date.today().isoformat()} -->")
    lines.append("")

    # Summary table (will be computed as we process domains)
    summary_rows = []

    # Process each domain
    for domain in sorted(endpoints_by_domain.keys()):
        endpoints = endpoints_by_domain[domain]
        implemented_ops = get_implemented_operation_ids(domain)

        # Separate implemented vs unimplemented
        implemented_list = []
        unimplemented_list = []

        for op_id in sorted(endpoints.keys()):
            if op_id in implemented_ops:
                implemented_list.append((op_id, implemented_ops[op_id]))
            else:
                unimplemented_list.append(op_id)

        # Compute statistics
        total_count = len(endpoints)
        implemented_count = len(implemented_list)
        unimplemented_count = len(unimplemented_list)

        # Count HIGH priority unimplemented
        high_priority_count = 0
        for op_id in unimplemented_list:
            _, priority = classify_endpoint(
                op_id,
                endpoints[op_id]['path'],
                endpoints[op_id]['method']
            )
            if priority == 'HIGH':
                high_priority_count += 1

        # Add to summary
        summary_rows.append({
            'domain': domain.replace('_', ' ').title(),
            'total': total_count,
            'implemented': implemented_count,
            'unimplemented': unimplemented_count,
            'high_priority': high_priority_count,
        })

        # Domain section
        lines.append(f"## {domain.replace('_', ' ').title()}")
        lines.append("")

        # 1. Total endpoint count
        lines.append(f"**Total Endpoints:** {total_count}")
        lines.append("")

        # 2. Implemented methods
        lines.append("**Implemented Methods:**")
        if implemented_list:
            for op_id, method_name in implemented_list:
                lines.append(f"- `{method_name}` → {op_id}")
        else:
            lines.append("*(none)*")
        lines.append("")

        # 3. Unimplemented endpoints
        lines.append("**Unimplemented Endpoints:**")
        if unimplemented_list:
            # Group by category
            by_category = {}
            for op_id in unimplemented_list:
                category, priority = classify_endpoint(
                    op_id,
                    endpoints[op_id]['path'],
                    endpoints[op_id]['method']
                )
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append((op_id, priority))

            for category in sorted(by_category.keys()):
                lines.append(f"\n**{category}:**")
                for op_id, priority in sorted(by_category[category]):
                    endpoint = endpoints[op_id]
                    lines.append(
                        f"- {priority}: `{endpoint['method']} {endpoint['path']}` ({op_id})"
                    )
        else:
            lines.append("*(none)*")
        lines.append("")

        # 4. Category breakdown
        lines.append("**Category Breakdown:**")
        category_counts = {}
        for op_id in unimplemented_list:
            category, _ = classify_endpoint(
                op_id,
                endpoints[op_id]['path'],
                endpoints[op_id]['method']
            )
            category_counts[category] = category_counts.get(category, 0) + 1

        if category_counts:
            for category in sorted(category_counts.keys()):
                lines.append(f"- {category}: {category_counts[category]}")
        else:
            lines.append("*(no unimplemented endpoints)*")
        lines.append("")

        # 5. Priority distribution
        lines.append("**Priority Distribution:**")
        priority_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for op_id in unimplemented_list:
            _, priority = classify_endpoint(
                op_id,
                endpoints[op_id]['path'],
                endpoints[op_id]['method']
            )
            priority_counts[priority] += 1

        lines.append(f"- HIGH: {priority_counts['HIGH']}")
        lines.append(f"- MEDIUM: {priority_counts['MEDIUM']}")
        lines.append(f"- LOW: {priority_counts['LOW']}")
        lines.append("")

    # Insert summary table at the top (after header)
    if summary_rows:
        summary_lines = [
            "",
            "## Summary",
            "",
            "| Domain | Total Endpoints | Implemented | Unimplemented | HIGH Priority |",
            "|--------|-----------------|-------------|---------------|---------------|",
        ]
        for row in summary_rows:
            summary_lines.append(
                f"| {row['domain']} | {row['total']} | {row['implemented']} | {row['unimplemented']} | {row['high_priority']} |"
            )
        summary_lines.append("")

        # Insert after header
        lines = lines[:4] + summary_lines + lines[4:]

    return '\n'.join(lines)


def main():
    """Main entry point."""
    spec_path = 'openapi/harness-openapi-normalized.yaml'
    output_path = 'docs/p1_endpoint_inventory.md'
    target_domains = ['pipelines', 'connectors', 'secrets']

    logger.info("Extracting endpoints for domains: %s", ', '.join(target_domains))

    try:
        endpoints_by_domain = extract_endpoints(spec_path, target_domains)
    except Exception as e:
        logger.error("Error extracting endpoints: %s", e)
        return 1

    # Verify we got endpoints for all target domains
    for domain in target_domains:
        count = len(endpoints_by_domain.get(domain, {}))
        logger.info("%s: %d endpoints with schemas", domain, count)

    # Generate markdown
    markdown_output = generate_inventory_md(endpoints_by_domain)

    # Write output
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        logger.info("Inventory written to: %s", output_path)
    except Exception as e:
        logger.error("Error writing output: %s", e)
        return 1

    # Print summary
    total_unimplemented = sum(
        sum(1 for op_id in endpoints_by_domain[domain]
            if op_id not in get_implemented_operation_ids(domain))
        for domain in target_domains
    )
    print(f"Endpoint inventory generated: {output_path}")
    print(f"Total unimplemented endpoints: {total_unimplemented}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
