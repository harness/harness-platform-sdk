# Harness Platform SDK

A production-grade Python SDK for the Harness platform API. Built with Pydantic v2, httpx, and comprehensive test coverage.

## Quick Start

```python
from harness_platform_sdk import HarnessClient

# Create a client
client = HarnessClient(
    api_key="your-api-key",
    account_id="your-account-id",
    default_org="your-org",
    default_project="your-project"
)

# Use context manager for automatic cleanup
with client:
    # Access resource APIs
    orgs = client.organizations.list()
    for org in orgs:
        print(f"Organization: {org.identifier}")
```

## Installation

```bash
pip install harness-platform-sdk
```

## Architecture

### Core Modules

- **`HarnessClient`** — Main entry point for all API interactions
  - HTTP methods with built-in retry (429, 503)
  - Scope resolution (account/org/project)
  - URL template substitution
  - Pagination support (OFFSET and CURSOR styles)

- **`HarnessConfig`** — Configuration management
  - API key, account ID, base URL
  - Timeout, retry settings
  - SSL verification control

- **`Scope`** — Request context model
  - Frozen Pydantic model
  - Account ID (required), org/project (optional)

- **Exception Hierarchy**
  - `HarnessSdkError` — Base exception
  - `ScopeNotSetError` — Missing required scope fields
  - `ApiError` — Non-2xx responses (with status, body, headers)
  - `AuthError` — 401/403 responses

- **`PaginationStyle`** — Pagination type enum
  - `OFFSET` — pageIndex/pageSize pagination
  - `CURSOR` — nextPageToken pagination

### Resource APIs

The SDK includes typed API wrappers for Harness platform resources across multiple domains:

- **Next-Gen (Core):** Organizations, Projects, Services, Service Overrides, Connectors, Secrets, Infrastructures, Variables, User Groups, Environments V2
- **Pipeline:** Pipelines (v0), Input Sets (v0), Triggers (v0), Templates (v0)
- **Authorization:** Roles, Resource Groups, Role Assignments
- **Infrastructure as Code:** Workspaces, Workspace Approvals, Workspace States, Workspace Variables, Workspace Default Pipelines
- **Internal Developer Portal:** Entities, Catalog Custom Properties, Scores

### Design Principles

1. **Single Entry Point** — All domain APIs are accessed via `HarnessClient`
2. **Scope Resolution** — Client automatically merges call-time and default scopes
3. **Type Safety** — Full Pydantic v2 models with validation
4. **Error Handling** — Explicit exception types with actionable messages
5. **Retry Logic** — Automatic retry on transient failures with exponential backoff
6. **No Async** — Pure sync using httpx (async support deferred to future version)

## Configuration

```python
from harness_platform_sdk import HarnessClient, HarnessConfig

# Option 1: Keyword arguments
client = HarnessClient(
    api_key="key",
    account_id="acc",
    default_org="my-org"
)

# Option 2: Explicit config
config = HarnessConfig(
    api_key="key",
    account_id="acc",
    base_url="https://app.harness.io",
    timeout=30.0,
    max_retries=3,
    retry_status_codes=[429, 503],
    retry_enabled=True,
    verify_ssl=True
)
client = HarnessClient(config=config)
```

## Error Handling

```python
from harness_platform_sdk import HarnessClient, AuthError, ApiError

client = HarnessClient(api_key="key", account_id="acc")

try:
    result = client._get("/some/endpoint")
except AuthError as e:
    print(f"Auth failed: {e.status_code}")
    # Handle 401/403
except ApiError as e:
    print(f"API error: {e.status_code}")
    # Handle other non-2xx
finally:
    client.close()
```

## Scope Management

```python
from harness_platform_sdk import HarnessClient, Scope

# Set default scope at construction
client = HarnessClient(
    api_key="key",
    account_id="acc",
    default_org="org-1",
    default_project="proj-1"
)

# Update default scope
client.set_default_scope(org="org-2", project="proj-2")

# Override scope for a specific call (future: when domain APIs are added)
# resource_manager.get(resource_id, scope=Scope(account_id="acc", org="org-temp"))
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## Testing

```bash
# Run all tests
mise run tests

# Run with coverage report
mise run tests:cov

# Run specific test file
pytest tests/unit_tests/test_client.py -v
```

## Version

- **Current:** 1.0.0
- **Stability:** Production-ready (v1.0.0 release)

## License

Business Source License 1.1 (BUSL-1.1) — See [License](License) for details.
