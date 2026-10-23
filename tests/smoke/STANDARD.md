# Smoke Test Documentation Standard

This document defines the standard structure and documentation format for Harness Platform SDK smoke tests.

## Purpose

Smoke tests validate end-to-end SDK functionality by exercising core API operations (List, Get, Create, Update, Delete) against a live Harness environment. Each test module covers one resource type and follows a consistent pattern for maintainability and clarity.

## File Naming Convention

- **Pattern:** `{resource_plural_lowercase}{_version}.py`
- **Examples:**
  - `organizations.py` — organization tests
  - `pipelines_v0.py` — v0 API pipeline tests
  - `input_sets_v0.py` — v0 API input set tests

## Module Docstring (Required)

Every test module must begin with a comprehensive docstring:

```python
"""
Smoke test for {ResourceName} API ({resource_description}).

Test Coverage:
  - List {resources}
  - Get {resource} by identifier
  - Create {resource}
  - Update {resource}
  - Delete {resource} (if cleanup=True)

Scope: {Scope: Account-level, Organization-level, or Project-level}
Fixture Dependency: {Foundation or Tier requirements}
"""
```

### Example:

```python
"""
Smoke test for Pipelines V0 API (pipeline CRUD operations).

Test Coverage:
  - List pipelines
  - Get pipeline by identifier
  - Create pipeline with stages and variables
  - Update pipeline (add stages)
  - Delete pipeline (if cleanup=True)

Scope: Project-level (requires org_id and project_id)
Fixture Dependency: Organizations, Projects (Tier 0-1)
"""
```

## Test Structure (Standard Pattern)

### 1. Setup Variables

```python
SUITE_NAME = "ResourceName"            # Display name for console output
SUITE_TEST_ID = "SDK_Test_ResourceName"   # Test resource identifier
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()  # Formatted name
SUITE_TEST_CLASS = client.resources    # API client class
```

### 2. Define Special Parameters (if needed)

```python
LIST_KWARGS = {}                       # Keyword args for .list() calls
GET_KWARGS = {}                        # Keyword args for .get() calls
DELETE_KWARGS = {}                     # Keyword args for .delete() calls
```

Examples:
```python
# For pipeline-scoped resources
LIST_KWARGS = {"pipeline_identifier": "default_list_pipeline"}
GET_KWARGS = {"pipeline_identifier": "default_list_pipeline"}
DELETE_KWARGS = {"pipeline_identifier": "default_list_pipeline"}

# For simple cases with no extra params
LIST_KWARGS = {}
```

### 3. Print Test Header

```python
print(f"{f' {SUITE_NAME} ':#^40}")
```

This creates a centered, visually distinct section in console output.

### 4. List (Before Creating)

```python
print(f"{SUITE_NAME} -> List")
for list_resource in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
    print(f"\t \t -> : {list_resource.identifier}")
```

### 5. Create Request Object

```python
resource_request = ResourceCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    description="Smoke Test Validation - Create",
    # ... other required fields
)
```

### 6. Get-or-Create Logic

```python
# Attempt to get existing resource
resource = SUITE_TEST_CLASS.get(identifier=resource_request.identifier, **GET_KWARGS)
if resource:
    print(f"\t -> Get : {resource.identifier}")
    resource_request.description = "Smoke Test Validation - Update"
    resource = SUITE_TEST_CLASS.update(identifier=resource.identifier, body=resource_request)
    print(f"\t -> Updated : {resource.identifier}")
else:
    # Create if not found
    resource = SUITE_TEST_CLASS.create(resource_request)
    print(f"\t -> Created : {resource.identifier}")
    resource_request.description = "Smoke Test Validation - Update after create"
    resource = SUITE_TEST_CLASS.update(identifier=resource.identifier, body=resource_request)
    print(f"\t -> Updated : {resource.identifier}")
```

**Why this pattern?**
- Tests are idempotent: safe to run repeatedly
- If a resource already exists from a prior run, the test verifies it can be fetched and updated
- If missing, the test verifies create + update workflows
- Consistent test coverage regardless of prior state

### 7. List (After Creating)

```python
print(f"{SUITE_NAME} -> List")
for list_resource in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
    print(f"\t \t -> : {list_resource.identifier}")
```

Verifies that the resource appears in list results after creation/update.

### 8. Cleanup (Conditional)

```python
if cleanup or unit_cleanup:
    SUITE_TEST_CLASS.delete(identifier=resource.identifier, **DELETE_KWARGS)
    print(f"\t -> Delete : {resource.identifier}")
```

**When to delete:**
- `cleanup` flag: delete test-scoped resources created by this test
- `unit_cleanup` flag: delete both test-scoped and unit-scoped resources
- Use `or` to trigger on either flag (test-scoped cleanup takes priority)

## Global Variables Available

These variables are injected by `scripts/run_smoke_tests.py` into each test module's global namespace:

```python
client                           # Authenticated HarnessClient instance
global_org_id                    # "PLATFORM_SDK_FIXTURES"
global_org_name                  # "Platform Sdk Fixtures"
global_project_id                # "FIXTURE_PLACEHOLDER"
global_project_name              # "Fixture Placeholder"
global_project_pipeline_id       # "default_list_pipeline"
global_project_environment_id    # "default_list_environment"
global_project_connector         # "default_list_connector"
global_project_secret            # "default_list_secret"
global_project_workspace         # "default_list_workspace"
global_catalog_entity            # "default_idp_catalog_entity"
global_idp_scorecard_check       # "default_idp_scorecard_check"
global_idp_scorecard             # "default_idp_scorecard"

cleanup                          # Boolean flag from CLI --cleanup
unit_cleanup                     # Boolean flag from CLI --unit-cleanup
```

## Scope Levels

Tests are scoped based on the required Harness scope:

| Scope | Description | Example |
|-------|-------------|---------|
| Account | No org/project required | Organizations, Projects |
| Organization | Requires org_id | Roles, Resource Groups (org-level) |
| Project | Requires org_id and project_id | Pipelines, Services, Connectors |

The client's default scope (set by run_smoke_tests.py) is `org=global_org_id, project=global_project_id`.

## Commenting Guidelines

### Bad (Obvious comments, noise):

```python
# Loop through pipelines
for pipeline in pipelines:
    print(pipeline.name)
```

### Good (Explains why or intent):

```python
# Attempt to get existing resource (tests are idempotent)
resource = SUITE_TEST_CLASS.get(identifier=resource_request.identifier, **GET_KWARGS)
```

### Add comments for:
- Non-obvious logic (e.g., why a specific parameter is used)
- Workarounds or special cases
- Complex nested structures
- Cross-references to fixtures

### Avoid comments for:
- What the code does (variable names and function names should be clear)
- Obvious loops and conditionals

## Resource Identifier Naming

Test resource identifiers should follow this pattern:

- **Standard tests:** `SDK_Test_{ResourceType}` (e.g., `SDK_Test_Pipeline`)
- **Fixture tests:** Align with fixture identifiers in `.terraform/` (e.g., `PLATFORM_SDK_FIXTURES`)

This makes it easy to identify test-created resources in a live account and facilitates cleanup.

## Error Handling

Smoke tests do **not** include explicit error handling for expected failures. If an API call fails:
1. The exception propagates
2. The test runner reports the failure with the full traceback
3. Other tests in the tier are skipped (tier-based orchestration stops)

This design ensures that unexpected failures are visible and blocks dependent tests from running.

## Testing Workflow

1. **Development:**
   ```bash
   python scripts/run_smoke_tests.py --filter-type pipelines
   ```

2. **Full suite run:**
   ```bash
   python scripts/run_smoke_tests.py
   ```

3. **With cleanup:**
   ```bash
   python scripts/run_smoke_tests.py --cleanup
   ```

4. **Review test output:**
   - Check console for section headers and operation results
   - Verify all resource identifiers are printed
   - Confirm cleanup messages appear if `--cleanup` flag was used

## Tier Ordering

Test tiers are defined in `.test_order.yaml` to enforce dependency ordering:

- **Tier 0 (foundation):** Organizations
- **Tier 1:** Projects, Pipelines, Environments, Secrets, Connectors
- **Tier 2:** Templates, Input Sets, Variables
- **Tier 3:** Workspaces, IDP Entities, Scorecards

A test's tier should reflect its resource dependencies. If your test depends on pipelines (Tier 1), put it in Tier 2 or higher.

## Generated Tests (Template-based)

For resources following the standard pattern, use the Jinja2 template:

```bash
# Generate a new test from the template
cp templates/base_smoke_test.py.j2 tests/smoke/new_resource.py
# Edit to customize CLASS_NAME_PREFIX, CLASS_VERSION, and resource-specific parameters
```

After generation:
1. Replace template variables with actual values
2. Add the test to `.test_order.yaml` under the appropriate tier
3. Run the test to verify it works

See `templates/base_smoke_test.py.j2` for the template.

## Debugging Tips

**Test hangs:** Check that fixture resources (org, project, pipelines) are provisioned:
```bash
cd tests/fixtures/terraform
tofu apply
```

**Resource not found:** Verify the resource identifier matches fixture definitions and smoke test references.

**Import errors:** Ensure all model classes are imported at the top of the test file.

**Cleanup not working:** Check that `cleanup` or `unit_cleanup` flags are set and delete operations are in the test.

## References

- [Harness Platform SDK Documentation](../../README.md)
- [Smoke Test Runner](../../scripts/run_smoke_tests.py)
- [Terraform Fixtures](../fixtures/terraform/README.md)
- [Base Test Template](../../templates/base_smoke_test.py.j2)
