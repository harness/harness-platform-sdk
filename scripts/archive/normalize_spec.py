# GENERATED — do not edit. Run mise run regenerate to update.
#!/usr/bin/env python3
from harness_python_sdk.base_model import HarnessModel
"""
Normalize Harness OpenAPI spec by fixing known quality defects.

Fixes:
1. Malformed 'required' fields (property-level -> schema-level)
2. Broken discriminator mappings (remove non-existent schema refs)
3. Empty schemas (add empty properties dict)
4. Inline response promotion (generate refs for inline schemas)
5. Dotted schema name flattening (prefix CamelCase + preserve suffix casing)

Outputs:
- openapi/harness-openapi-normalized.yaml
- scripts/inline_response_map.json
- docs/spec_repairs.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from collections import defaultdict

import yaml


INPUT_SPEC = Path(__file__).parent.parent / "openapi" / "harness-openapi.yaml"
OUTPUT_SPEC = Path(__file__).parent.parent / "openapi" / "harness-openapi-normalized.yaml"
INLINE_MAP = Path(__file__).parent / "inline_response_map.json"
REPAIRS_LOG = Path(__file__).parent.parent / "docs" / "spec_repairs.json"

# Ensure docs directory exists
REPAIRS_LOG.parent.mkdir(parents=True, exist_ok=True)


class SpecNormalizer:
    """Normalizes OpenAPI spec with targeted fixes."""

    def __init__(self, spec_dict: Dict[str, Any]):
        self.spec = spec_dict
        self.repairs = {
            "malformed_required": [],
            "broken_discriminator": [],
            "empty_schema": [],
            "inline_response_promotions": [],
            "dotted_schema_renames": [],
            "discriminators_removed": 0,
        }
        self.inline_response_map = {}
        self._operation_counter = 0

    def normalize(self) -> Dict[str, Any]:
        """Run all fixes in sequence."""
        self._fix_dotted_schema_names()
        self._fix_malformed_required()
        self._fix_broken_discriminators()
        self._remove_all_discriminators()
        self._fix_empty_schemas()
        self._promote_inline_responses()
        return self.spec

    def _make_flat_name(self, old_name: str) -> str:
        """Convert a dotted schema name to flat PascalCase.

        Preserves the exact casing of the suffix (part after the last dot).
        Converts the prefix to CamelCase from snake_case/kebab-case.

        Examples:
            action.ActionTemplateProperties
                -> ActionActionTemplateProperties
            github_com_harness_hce-saas_graphql_server_api.Pagination
                -> GithubComHarnessHceSaasGraphqlServerApiPagination
        """
        dot_pos = old_name.rfind('.')
        prefix_raw = old_name[:dot_pos]
        suffix = old_name[dot_pos + 1:]
        prefix_clean = prefix_raw.replace('-', '_')
        prefix_camel = ''.join(w.capitalize() for w in prefix_clean.split('_') if w)
        return prefix_camel + suffix[0].upper() + suffix[1:]

    def _fix_dotted_schema_names(self) -> None:
        """Fix dotted-prefix schema names to flat PascalCase.

        Schemas with dots in names (e.g., 'action.ActionTemplateProperties',
        'github_com_harness_hce-saas_graphql_server_api.Pagination') confuse the
        generator's module-resolution logic and cause flat-named schemas to be
        silently dropped. This fix renames all dotted schemas to flat PascalCase
        before generation.
        """
        schemas = self.spec.get("components", {}).get("schemas", {})

        # Collect all dotted schema names
        dotted_schemas = [name for name in schemas if '.' in name]
        if not dotted_schemas:
            return

        # Build rename map with collision detection
        rename_map = {}
        collision_counter = defaultdict(int)

        for old_name in dotted_schemas:
            # Generate flat PascalCase name using correct algorithm
            new_name = self._make_flat_name(old_name)

            # Handle collisions with counter suffix
            check_name = new_name
            if check_name in schemas and check_name not in rename_map.values():
                collision_counter[new_name] += 1
                check_name = f"{new_name}_{collision_counter[new_name]}"

            # Continue incrementing if collision persists
            while check_name in schemas and check_name not in rename_map.values():
                collision_counter[new_name] += 1
                check_name = f"{new_name}_{collision_counter[new_name]}"

            rename_map[old_name] = check_name
            self.repairs["dotted_schema_renames"].append({
                "old": old_name,
                "new": check_name,
            })

        # Pass 1: Rename keys in components/schemas
        for old_name, new_name in rename_map.items():
            if old_name in schemas:
                schemas[new_name] = schemas.pop(old_name)

        # Pass 2: Replace all schema references using JSON string manipulation
        # This ensures we catch all references including those in nested structures
        spec_json = json.dumps(self.spec)
        for old_name, new_name in rename_map.items():
            old_ref = f'"#/components/schemas/{old_name}"'
            new_ref = f'"#/components/schemas/{new_name}"'
            spec_json = spec_json.replace(old_ref, new_ref)

        # Reload spec from modified JSON
        self.spec = json.loads(spec_json)

    def _fix_malformed_required(self) -> None:
        """Fix 1: Move property-level 'required: true' to schema-level 'required' array."""
        schemas = self.spec.get("components", {}).get("schemas", {})

        def fix_schema(schema: Dict[str, Any], schema_name: str) -> None:
            if not isinstance(schema, dict):
                return

            properties = schema.get("properties", {})
            if not isinstance(properties, dict):
                return

            required = set(schema.get("required", []))
            fields_to_remove = []

            for field_name, field_def in properties.items():
                if isinstance(field_def, dict) and field_def.get("required") is True:
                    required.add(field_name)
                    fields_to_remove.append(field_name)
                    self.repairs["malformed_required"].append({
                        "schema": schema_name,
                        "field": field_name,
                    })

            # Remove property-level 'required: true'
            for field_name in fields_to_remove:
                del properties[field_name]["required"]

            # Update schema-level required
            if required:
                schema["required"] = sorted(list(required))
            elif "required" in schema and not required:
                del schema["required"]

        # Fix schemas in components/schemas
        for schema_name, schema_def in schemas.items():
            fix_schema(schema_def, schema_name)

            # Also fix nested inline schemas in allOf/anyOf/oneOf
            for combiner in ["allOf", "anyOf", "oneOf"]:
                if combiner in schema_def:
                    for i, sub_schema in enumerate(schema_def[combiner]):
                        if isinstance(sub_schema, dict) and "properties" in sub_schema:
                            fix_schema(sub_schema, f"{schema_name}#{combiner}[{i}]")

        # Fix schemas in request bodies and responses
        paths = self.spec.get("paths", {})
        for path_key, path_item in paths.items():
            for method, operation in path_item.items():
                if not isinstance(operation, dict):
                    continue

                # Check requestBody
                request_body = operation.get("requestBody", {})
                if isinstance(request_body, dict):
                    for content_type, content in request_body.get("content", {}).items():
                        if isinstance(content, dict):
                            schema = content.get("schema", {})
                            if isinstance(schema, dict) and "properties" in schema:
                                fix_schema(schema, f"{path_key}#{method}#requestBody")

                # Check responses
                responses = operation.get("responses", {})
                for status_code, response in responses.items():
                    if isinstance(response, dict):
                        for content_type, content in response.get("content", {}).items():
                            if isinstance(content, dict):
                                schema = content.get("schema", {})
                                if isinstance(schema, dict) and "properties" in schema:
                                    fix_schema(schema, f"{path_key}#{method}#response[{status_code}]")

    def _fix_broken_discriminators(self) -> None:
        """Fix 2: Remove discriminator mappings to non-existent schemas."""
        schemas = self.spec.get("components", {}).get("schemas", {})

        def fix_discriminator(obj: Dict[str, Any], schema_name: str) -> None:
            if not isinstance(obj, dict):
                return

            if "discriminator" in obj and isinstance(obj["discriminator"], dict):
                discriminator = obj["discriminator"]
                if "mapping" in discriminator and isinstance(discriminator["mapping"], dict):
                    original_mappings = set(discriminator["mapping"].keys())
                    removed_mappings = []

                    # Filter to only mappings that reference existing schemas
                    valid_mappings = {}
                    for key, schema_ref in discriminator["mapping"].items():
                        # Extract schema name from ref (e.g., "#/components/schemas/MySchema" -> "MySchema")
                        if schema_ref.startswith("#/components/schemas/"):
                            ref_name = schema_ref.split("/")[-1]
                            if ref_name in schemas:
                                valid_mappings[key] = schema_ref
                            else:
                                removed_mappings.append(key)
                        else:
                            # Keep non-standard refs as-is
                            valid_mappings[key] = schema_ref

                    if removed_mappings:
                        self.repairs["broken_discriminator"].append({
                            "schema": schema_name,
                            "removed_mappings": removed_mappings,
                        })

                    # Update or remove mapping
                    if valid_mappings:
                        discriminator["mapping"] = valid_mappings
                    else:
                        # No valid mappings left
                        if "mapping" in discriminator:
                            del discriminator["mapping"]
                        # If discriminator has no other content, remove it
                        if not discriminator or discriminator == {"mapping": {}}:
                            del obj["discriminator"]

        # Fix all schemas
        for schema_name, schema_def in schemas.items():
            fix_discriminator(schema_def, schema_name)

            # Also check nested schemas
            for combiner in ["allOf", "anyOf", "oneOf"]:
                if combiner in schema_def and isinstance(schema_def[combiner], list):
                    for i, sub_schema in enumerate(schema_def[combiner]):
                        if isinstance(sub_schema, dict):
                            fix_discriminator(sub_schema, f"{schema_name}#{combiner}[{i}]")

        # Additional fix: identify schemas that reference a parent schema with a discriminator
        # but have x-discriminator-value not in the parent's mapping (incomplete discriminators)
        # This prevents code generation errors when parent schemas with incomplete discriminators
        # are processed
        schemas_with_discriminator_values = {}
        for schema_name, schema_def in schemas.items():
            if isinstance(schema_def, dict) and "x-discriminator-value" in schema_def:
                schemas_with_discriminator_values[schema_name] = schema_def["x-discriminator-value"]

        # Find schemas with discriminators that have issues
        # Issues include:
        # 1. Missing mappings (child schema refs not in mapping)
        # 2. Mismatched mapping (mapping values don't match actual child schema names)
        incomplete_discriminators = set()
        orphaned_discriminator_values = []

        for schema_name, schema_def in schemas.items():
            if not isinstance(schema_def, dict) or "discriminator" not in schema_def:
                continue

            discriminator = schema_def.get("discriminator", {})
            if not isinstance(discriminator, dict):
                continue

            mapping = discriminator.get("mapping", {})
            if not isinstance(mapping, dict):
                continue

            # Find all schemas that reference this schema (via $ref) or inherit from it
            for other_name, other_def in schemas.items():
                if not isinstance(other_def, dict):
                    continue

                all_of = other_def.get("allOf", [])
                if not isinstance(all_of, list):
                    continue

                # Check if this schema references the discriminator schema
                references_discriminator = any(
                    isinstance(item, dict) and item.get("$ref") == f"#/components/schemas/{schema_name}"
                    for item in all_of
                )

                if not references_discriminator:
                    continue

                # Check if this schema has an x-discriminator-value (now removed but check for safety)
                disc_value = other_def.get("x-discriminator-value")

                # Check for mapping mismatch: if the mapping target schema doesn't exist
                # or the child schema name doesn't appear in any mapping value, it's broken
                mapping_has_child = any(
                    v.endswith(f"/{other_name}") if v.startswith("#/components/schemas/") else False
                    for v in mapping.values()
                )

                if disc_value and disc_value not in mapping:
                    incomplete_discriminators.add(schema_name)
                    orphaned_discriminator_values.append({
                        "schema": other_name,
                        "x_discriminator_value": disc_value,
                        "parent_schema": schema_name
                    })
                elif not mapping_has_child and other_name not in [v.split("/")[-1] for v in mapping.values() if v.startswith("#/components/schemas/")]:
                    # Child schema name doesn't appear in mapping - remove discriminator
                    incomplete_discriminators.add(schema_name)

        # Remove incomplete discriminators
        for schema_name in incomplete_discriminators:
            schema_def = schemas[schema_name]
            if "discriminator" in schema_def:
                del schema_def["discriminator"]
                self.repairs["broken_discriminator"].append({
                    "schema": schema_name,
                    "removed_reason": "Incomplete discriminator: mapping doesn't include all child schemas",
                })

        # Also remove x-discriminator-value from orphaned child schemas
        for orphan_info in orphaned_discriminator_values:
            schema_name = orphan_info["schema"]
            if schema_name in schemas and isinstance(schemas[schema_name], dict):
                if "x-discriminator-value" in schemas[schema_name]:
                    del schemas[schema_name]["x-discriminator-value"]

        # Remove ALL x-discriminator-value from schemas to avoid code generation issues
        # These are OpenAPI extensions that can cause datamodel-code-generator failures
        # when discriminators are incomplete or improperly mapped
        for schema_name, schema_def in list(schemas.items()):
            if isinstance(schema_def, dict) and "x-discriminator-value" in schema_def:
                del schema_def["x-discriminator-value"]

    def _remove_all_discriminators(self) -> None:
        """Remove all remaining discriminators from the spec.

        Discriminators in the OpenAPI spec cause crashes in datamodel-code-generator
        when discriminator mappings are incomplete or not resolvable. Since HarnessModel
        uses extra="allow" for polymorphic payload handling, discriminators provide no
        value for the SDK and can be safely removed.
        """
        schemas = self.spec.get("components", {}).get("schemas", {})
        removed_count = 0

        def remove_discriminators_recursive(obj: Dict[str, Any]) -> int:
            """Recursively remove discriminators from object and nested schemas."""
            count = 0
            if not isinstance(obj, dict):
                return count

            # Remove discriminator from this object
            if "discriminator" in obj:
                del obj["discriminator"]
                count += 1

            # Remove from allOf/anyOf/oneOf sub-schemas
            for combiner in ["allOf", "anyOf", "oneOf"]:
                if combiner in obj and isinstance(obj[combiner], list):
                    for sub_schema in obj[combiner]:
                        if isinstance(sub_schema, dict):
                            count += remove_discriminators_recursive(sub_schema)

            return count

        # Remove discriminators from all top-level schemas
        for schema_name, schema_def in schemas.items():
            if isinstance(schema_def, dict):
                removed_count += remove_discriminators_recursive(schema_def)

        self.repairs["discriminators_removed"] = removed_count

    def _fix_empty_schemas(self) -> None:
        """Fix 3: Add empty 'properties: {}' to schemas with no content."""
        schemas = self.spec.get("components", {}).get("schemas", {})

        for schema_name, schema_def in schemas.items():
            if not isinstance(schema_def, dict):
                continue

            # Check if schema is empty (no properties, allOf, oneOf, anyOf, $ref)
            has_properties = "properties" in schema_def
            has_allof = "allOf" in schema_def
            has_oneof = "oneOf" in schema_def
            has_anyof = "anyOf" in schema_def
            has_ref = "$ref" in schema_def

            if not (has_properties or has_allof or has_oneof or has_anyof or has_ref):
                schema_def["properties"] = {}
                self.repairs["empty_schema"].append({"schema": schema_name})

    def _promote_inline_responses(self) -> None:
        """Fix 4: Promote inline response schemas to components/schemas with $ref."""
        schemas = self.spec.get("components", {}).get("schemas", {})
        paths = self.spec.get("paths", {})

        for path_key, path_item in paths.items():
            for method, operation in path_item.items():
                if not isinstance(operation, dict):
                    continue

                operation_id = operation.get("operationId", f"operation_{self._operation_counter}")
                self._operation_counter += 1

                responses = operation.get("responses", {})
                for status_code, response in responses.items():
                    if not isinstance(response, dict):
                        continue

                    content = response.get("content", {})
                    for content_type, content_def in content.items():
                        if not isinstance(content_def, dict):
                            continue

                        schema = content_def.get("schema")
                        if schema is None:
                            continue

                        # Check if schema is inline (not a $ref)
                        if isinstance(schema, dict) and "$ref" not in schema:
                            # Generate deterministic name
                            generated_name = f"{operation_id}_{status_code}_Response"

                            # Ensure name is unique
                            counter = 1
                            check_name = generated_name
                            while check_name in schemas:
                                check_name = f"{generated_name}_{counter}"
                                counter += 1
                            generated_name = check_name

                            # Register schema and replace with $ref
                            schemas[generated_name] = schema
                            content_def["schema"] = {"$ref": f"#/components/schemas/{generated_name}"}

                            self.repairs["inline_response_promotions"].append({
                                "generated_name": generated_name,
                                "operation_id": operation_id,
                                "status_code": status_code,
                            })

                            self.inline_response_map[generated_name] = {
                                "operation_id": operation_id,
                                "status_code": status_code,
                            }


def main():
    """Load, normalize, and save spec."""
    print(f"Loading spec from {INPUT_SPEC}...")
    with open(INPUT_SPEC, "r") as f:
        spec = yaml.safe_load(f)

    print("Normalizing spec...")
    normalizer = SpecNormalizer(spec)
    normalized_spec = normalizer.normalize()

    # Save normalized YAML
    print(f"Writing normalized spec to {OUTPUT_SPEC}...")
    with open(OUTPUT_SPEC, "w") as f:
        yaml.dump(normalized_spec, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

    # Save inline response map
    print(f"Writing inline response map to {INLINE_MAP}...")
    with open(INLINE_MAP, "w") as f:
        json.dump(normalizer.inline_response_map, f, indent=2)

    # Save repairs log with sorted entries and relative paths for idempotency
    # Sort each repair list by schema name for consistent output
    sorted_repairs = {}
    for key, value in normalizer.repairs.items():
        if isinstance(value, list):
            # Sort list entries by their 'schema' field if it exists
            if value and isinstance(value[0], dict) and 'schema' in value[0]:
                sorted_repairs[key] = sorted(value, key=lambda x: x.get('schema', ''))
            else:
                sorted_repairs[key] = value
        else:
            sorted_repairs[key] = value

    # Convert absolute path to relative path from repository root
    try:
        spec_relative = INPUT_SPEC.relative_to(Path(__file__).parent.parent)
    except ValueError:
        spec_relative = INPUT_SPEC

    repairs_log = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_spec": str(spec_relative),
        "repairs": sorted_repairs,
        "totals": {k: (v if isinstance(v, int) else len(v)) for k, v in sorted_repairs.items()},
    }
    print(f"Writing repairs log to {REPAIRS_LOG}...")
    with open(REPAIRS_LOG, "w") as f:
        json.dump(repairs_log, f, indent=2)

    # Print summary
    total_repairs = sum(v if isinstance(v, int) else len(v) for v in normalizer.repairs.values())
    print("\n" + "="*70)
    print("NORMALIZATION SUMMARY")
    print("="*70)
    print(f"Dotted schema names renamed: {len(normalizer.repairs['dotted_schema_renames'])}")
    print(f"Malformed 'required' fields fixed: {len(normalizer.repairs['malformed_required'])}")
    print(f"Broken discriminators fixed: {len(normalizer.repairs['broken_discriminator'])}")
    print(f"Discriminators removed: {normalizer.repairs['discriminators_removed']}")
    print(f"Empty schemas fixed: {len(normalizer.repairs['empty_schema'])}")
    print(f"Inline responses promoted: {len(normalizer.repairs['inline_response_promotions'])}")
    print(f"Total repairs: {total_repairs}")
    print("="*70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
