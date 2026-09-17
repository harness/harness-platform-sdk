# Contributing New Resource Classes

This guide describes how to add a new resource endpoint API class to the Harness Platform SDK using the automated code generation workflow.

## Overview

The SDK follows a consistent pattern for resource API classes. Each resource includes:
- An **API client class** (`<ResourceName>Api`) that manages HTTP operations
- **Pydantic data models** (`<ResourceName>CreateRequest`, `<ResourceName>Response`)
- **Smoke tests** for lifecycle validation (create, read, list, update, delete)

Use the `mise create:new` command to scaffold all files at once, then verify via smoke tests.

---

## Prerequisites

Before generating a new resource class, you need:

1. **API Endpoint Documentation** — The root API path and supported HTTP methods (GET, POST, PUT, DELETE)
2. **Response Structure Knowledge** — Understanding of the API response envelope (typically `{status, data}`)
3. **Domain Assignment** — Decision on which API module: `ng_api`, `authz`, `iacm_api`, `idp_api`, `pipeline_api`, or `template_api`
4. **Harness API Docs** — Reference to `.ai/harness_api_docs.md` or the upstream OpenAPI specification

---

## Step-by-Step Implementation

### Step 1: Gather API Information

**Do:**
- Locate the resource's root API path (e.g., `/v1/entities`, `/v2/projects`, `/api/pipelines`)
- Document supported HTTP methods: GET, POST, PUT, DELETE
- Verify response envelope structure (most Harness APIs use `{status: "string", data: {...}}`)
- Check if the resource requires scope parameters (account, org, project)
- Note any non-standard query parameters or headers

**Example:**
```
Resource: Organizations
Root Path: /orgs
Methods: GET (list, get), POST (create), PUT (update), DELETE (delete)
Scope: Account-level (no org/project)
Response: {status, data} wrapper
```

### Step 2: Choose API Module and Generate Class

**Do:**
- Run the generation command with your resource details:
  ```bash
  mise create:new \
    --endpoint-target <api_module> \
    --class-prefix <ResourceName> \
    --root-api-path "<api_path>"
  ```

**Parameters:**
- `--endpoint-target`: Domain module (`ng_api`, `authz`, `iacm_api`, `idp_api`, `pipeline_api`, `template_api`)
- `--class-prefix`: PascalCase resource name (e.g., `Organization`, `CatalogCustomProperty`)
- `--root-api-path`: Full API root path (e.g., `/v1/entities`, `/v2/projects`)

**Example:**
```bash
mise create:new \
  --endpoint-target ng_api \
  --class-prefix Service \
  --root-api-path "/v2/services"
```

**Files Generated:**
- `src/harness_platform_sdk/<api_module>/<resource_name>.py` — API client
- `src/harness_platform_sdk/models/<api_module>/<resource_name>.py` — Data models
- `tests/smoke/<resource_name>.py` — Smoke test

### Step 3: Review Generated Files

**Do:**
- Open each generated file and verify the structure matches existing patterns
- Check that the class has expected CRUD methods: `list()`, `get()`, `create()`, `update()`, `delete()`
- Verify models inherit from `HarnessModel` with correct Pydantic config
- Ensure request/response classes have proper type hints

**Expected Structure:**

**API Client (`src/harness_platform_sdk/<api_module>/<resource_name>.py`):**
```python
class <ResourceName>Api:
    def __init__(self, client: HarnessClient):
        """Initialize the resource API."""
        
    def list(self, **kwargs) -> Generator[<ResourceName>Response, None, None]:
        """List all resources."""
        
    def get(self, resource_id: str, **kwargs) -> <ResourceName>Response:
        """Get a specific resource."""
        
    def create(self, body: <ResourceName>CreateRequest, **kwargs) -> <ResourceName>Response:
        """Create a new resource."""
        
    def update(self, resource_id: str, body: <ResourceName>CreateRequest, **kwargs) -> <ResourceName>Response:
        """Update an existing resource."""
        
    def delete(self, resource_id: str, **kwargs) -> None:
        """Delete a resource."""
```

**Models (`src/harness_platform_sdk/models/<api_module>/<resource_name>.py`):**
```python
class <ResourceName>Response(HarnessModel):
    """Response model for <resource_name>."""
    # Fields matching API response structure
    
class <ResourceName>CreateRequest(HarnessModel):
    """Request model for creating/updating <resource_name>."""
    # Fields matching API request structure
```

### Step 4: Update API Module Exports

**Do:**
- Add the new resource to the API module's `__init__.py`
- Export the `<ResourceName>Api` class
- Example for `ng_api/__init__.py`:

```python
from .services import ServicesApi
from .service_overrides import ServiceOverridesApi  # New

__all__ = [
    "ServicesApi",
    "ServiceOverridesApi",  # New
]
```

### Step 5: Add Property to HarnessClient

**Do:**
- Open `src/harness_platform_sdk/client.py`
- Add a lazy-loaded property for the new resource:

```python
@property
def service_overrides(self) -> ServiceOverridesApi:
    """Access Service Overrides API."""
    if self._service_overrides is None:
        self._service_overrides = ServiceOverridesApi(self)
    return self._service_overrides
```

- Add the private cache variable in `__init__`:
```python
self._service_overrides: ServiceOverridesApi | None = None
```

### Step 6: Write/Update Smoke Test

**Do:**
- The smoke test is auto-generated, but may need environment setup
- Add test account ID, organization, project from environment variables or test fixtures
- Ensure the smoke test covers:
  - Resource creation with minimal valid fields
  - Resource retrieval by ID
  - Resource listing
  - Resource update
  - Resource deletion
  - Error cases (404, 400, 401)

**Example smoke test structure:**
```python
def test_service_overrides_lifecycle():
    """Test full CRUD lifecycle for service overrides."""
    client = HarnessClient(api_key=API_KEY, account_id=ACCOUNT_ID)
    
    # Create
    req = ServiceOverrideCreateRequest(name="test-override", spec={...})
    resp = client.service_overrides.create(req)
    assert resp.identifier == "test-override"
    
    # Read
    retrieved = client.service_overrides.get(resp.identifier)
    assert retrieved.identifier == "test-override"
    
    # List
    items = list(client.service_overrides.list())
    assert len(items) > 0
    
    # Update
    req.spec = {...}  # Updated spec
    updated = client.service_overrides.update(resp.identifier, req)
    assert updated.spec == {...}
    
    # Delete
    client.service_overrides.delete(resp.identifier)
```

### Step 7: Run Tests

**Do:**
- Run the smoke test:
  ```bash
  pytest tests/smoke/<resource_name>.py -v
  ```
- Run the full test suite to ensure no regressions:
  ```bash
  pytest tests/ -v
  ```
- If tests fail, check:
  - API credentials (API key, account ID)
  - Endpoint availability (may require staging environment)
  - Request/response model alignment with actual API

**Expected outcome:**
- All smoke tests pass, OR
- Failure documented with root cause (e.g., endpoint not available in test environment)

### Step 8: Verify Type Safety and Docstrings

**Do:**
- Ensure all methods have Google-style docstrings:
  ```bash
  ruff check --select D src/harness_platform_sdk/<api_module>/<resource_name>.py
  ```
- Check type hints are complete:
  ```bash
  mypy src/harness_platform_sdk/<api_module>/<resource_name>.py
  ```
- Run docstring examples (if present):
  ```bash
  pytest --doctest-modules src/harness_platform_sdk/<api_module>/<resource_name>.py -v
  ```

---

## Architectural Patterns

### Resource API Class Pattern

All resource API classes follow this pattern:

```python
from harness_platform_sdk import HarnessClient
from harness_platform_sdk.models.<api_module>.<resource_name> import (
    <ResourceName>Response,
    <ResourceName>CreateRequest,
)

class <ResourceName>Api:
    def __init__(self, client: HarnessClient):
        self._client = client
        
    def list(self, **kwargs) -> Generator[<ResourceName>Response, None, None]:
        """List all resources."""
        # Typically: GET /<root_api_path> with pagination
        
    def get(self, resource_id: str, **kwargs) -> <ResourceName>Response:
        """Get a specific resource by ID."""
        # GET /<root_api_path>/{resource_id}
        
    def create(self, body: <ResourceName>CreateRequest, **kwargs) -> <ResourceName>Response:
        """Create a new resource."""
        # POST /<root_api_path>
        
    def update(self, resource_id: str, body: <ResourceName>CreateRequest, **kwargs) -> <ResourceName>Response:
        """Update an existing resource."""
        # PUT /<root_api_path>/{resource_id}
        
    def delete(self, resource_id: str, **kwargs) -> None:
        """Delete a resource."""
        # DELETE /<root_api_path>/{resource_id}
```

### Response Envelope Handling

Most Harness APIs return responses wrapped in a status envelope:

```json
{
  "status": "SUCCESS",
  "data": {
    "identifier": "resource-id",
    "name": "Resource Name",
    ...
  }
}
```

The generated code automatically unwraps this using the `unwrap_field` parameter in `_get()`, `_post()`, etc.

### Pagination Support

For list endpoints returning multiple items:

```python
def list(self, **kwargs) -> Generator[<ResourceName>Response, None, None]:
    """List resources with automatic pagination."""
    return self._client._paginate(
        method="GET",
        path="/v1/<resources>",
        response_model=<ResourceName>Response,
        unwrap_field="data",  # Extract from envelope
        **kwargs
    )
```

### Scope Handling

For resources requiring account/org/project context:

```python
def get(self, resource_id: str, scope: Scope | None = None, **kwargs) -> <ResourceName>Response:
    """Get resource with optional scope override."""
    scope = self._client._resolve_scope(scope)
    path = f"/api/v2/accounts/{scope.account_id}/orgs/{scope.org}/projects/{scope.project}/<resources>/{resource_id}"
    return self._client._get(path, response_model=<ResourceName>Response, **kwargs)
```

---

## Common Patterns & Tips

### 1. Non-Standard HTTP Methods

Some endpoints may use unusual patterns:
- **Query operations** via POST: `POST /v1/resources/query` with filters in body
- **Bulk operations**: `POST /v1/resources/bulk-delete` with IDs in body
- **Complex reads**: `POST /v1/resources/search` instead of GET

Adapt the API class methods to match the actual API patterns.

### 2. Conditional CRUD Operations

Some resources may lack certain operations:
- Read-only APIs (GET/list only, no create/update/delete)
- Write-only APIs (POST only)
- No delete operation

Generate only the relevant methods:

```python
class ReadOnlyApi:
    def list(self, **kwargs) -> Generator[...]:
        ...
        
    def get(self, resource_id: str, **kwargs) -> ...:
        ...
        
    # No create, update, delete
```

### 3. Pagination Styles

Harness APIs use two pagination patterns:

**Offset-based (OFFSET):**
```python
return self._client._paginate(
    ...,
    pagination_style=PaginationStyle.OFFSET,  # pageIndex/pageSize
    ...
)
```

**Cursor-based (CURSOR):**
```python
return self._client._paginate(
    ...,
    pagination_style=PaginationStyle.CURSOR,  # nextPageToken
    ...
)
```

### 4. Error Handling

The client automatically maps HTTP errors to SDK exceptions:
- `401/403` → `AuthError`
- `404` → `ApiError` (check response for details)
- `4xx/5xx` → `ApiError`
- Missing scope → `ScopeNotSetError`

No additional error handling needed in generated code.

---

## Testing Checklist

Before committing new resource classes, verify:

- [ ] API client class generated with correct name (`<ResourceName>Api`)
- [ ] Methods present: `list()`, `get()`, `create()`, `update()`, `delete()` (or subset as appropriate)
- [ ] Request/response models inherit from `HarnessModel`
- [ ] Models have Google-style docstrings
- [ ] Smoke test file created and executable
- [ ] Smoke test covers create→read→list→update→delete lifecycle
- [ ] Type hints complete across all methods
- [ ] No ruff/mypy/doctest warnings
- [ ] Client property added and accessible via `client.<resource_name>`
- [ ] Full test suite passes: `pytest tests/ -v`
- [ ] Generated files follow existing code style
- [ ] No manual modifications needed beyond documentation

---

## Troubleshooting

### Generation Command Fails

**Error:** `mise create:new: command not found`
- **Cause:** Task not defined in `mise.toml`
- **Fix:** Check that `mise.toml` has `create:new` task defined, or use alternative generation method

**Error:** Invalid `--endpoint-target`
- **Cause:** API module doesn't exist
- **Fix:** Use valid module: `ng_api`, `authz`, `iacm_api`, `idp_api`, `pipeline_api`, `template_api`

### Smoke Test Fails

**Error:** `AuthError: 401 Unauthorized`
- **Cause:** Invalid API key or account ID
- **Fix:** Verify `HARNESS_API_KEY` and `HARNESS_ACCOUNT_ID` environment variables

**Error:** `ApiError: 404 Not Found`
- **Cause:** Endpoint not available or wrong path
- **Fix:** Check API path in generated class matches actual Harness API docs

**Error:** `ScopeNotSetError`
- **Cause:** Test missing required scope (org, project)
- **Fix:** Set default scope in client construction or pass explicitly to method

### Model Validation Fails

**Error:** `ValidationError: field required`
- **Cause:** Request model missing required fields
- **Fix:** Check API docs for required fields, update models or smoke test

---

## Real-World Example: Adding Service Overrides

Here's a complete walkthrough:

**1. Gather Info:**
```
Resource: Service Overrides (v2 API)
Root Path: /api/v2/service-overrides
Methods: GET (list, get), POST (create), PUT (update), DELETE (delete)
Scope: Account + Org + Project
Response: {status, data} wrapper
```

**2. Generate:**
```bash
mise create:new \
  --endpoint-target ng_api \
  --class-prefix ServiceOverride \
  --root-api-path "/api/v2/service-overrides"
```

**3. Update `ng_api/__init__.py`:**
```python
from .service_overrides import ServiceOverridesApi

__all__ = [..., "ServiceOverridesApi"]
```

**4. Update `client.py`:**
```python
@property
def service_overrides(self) -> ServiceOverridesApi:
    """Access Service Overrides API."""
    if self._service_overrides is None:
        self._service_overrides = ServiceOverridesApi(self)
    return self._service_overrides
```

**5. Run smoke test:**
```bash
pytest tests/smoke/service_overrides.py -v
```

**6. Verify type safety:**
```bash
ruff check --select D src/harness_platform_sdk/ng_api/service_overrides.py
pytest --doctest-modules src/harness_platform_sdk/ng_api/service_overrides.py -v
```

**7. Commit and create PR!**

---

## References

- **WorkspaceVariables Pattern:** `src/harness_platform_sdk/iacm_api/workspace_variables.py`
- **HarnessClient:** `src/harness_platform_sdk/client.py`
- **Base Models:** `src/harness_platform_sdk/base_model.py`
- **API Docs:** `.ai/harness_api_docs.md`
- **Test Examples:** `tests/smoke/` and `tests/unit_tests/`
- **Docstring Guide:** `docs/DOCSTRING_STYLE.md`
