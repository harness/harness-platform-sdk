# Harness Platform SDK

> Python SDK for the Harness Platform API. Full-featured client library with authentication, scope management, pagination, retry handling, and comprehensive type hints for accurate code generation.


## Quick Start

- [Installation & Setup](/docs/generated/index.md#installation)
- [Authentication](/docs/generated/index.md#authentication)
- [Basic Usage Example](/docs/generated/index.md#basic-usage)

## Core Concepts

- [Scope Management](/docs/generated/index.md#scope) — Account, Organization, Project hierarchy
- [HTTP Methods](/docs/generated/index.md#http-methods) — GET, POST, PUT, PATCH, DELETE with retry
- [Error Handling](/docs/generated/index.md#error-handling) — Exception types and scenarios
- [Pagination](/docs/generated/index.md#pagination) — Offset and cursor-based pagination

## API Reference

### Client Initialization

- [HarnessClient](/docs/generated/index.md#harnessclient) — Main entry point
- [HarnessConfig](/docs/generated/index.md#harnessconfig) — Configuration object
- [Scope](/docs/generated/index.md#scope) — Scope definition

### API Managers (Lazy-Loaded)

#### Next Generation API (NG)

- [ConnectorsApi](/docs/generated/index.md#connectorsapi) — Manage connectors
- [EnvironmentsV2Api](/docs/generated/index.md#environmentsv2api) — Manage environments_v2
- [InfrastructuresApi](/docs/generated/index.md#infrastructuresapi) — Manage infrastructures
- [OrganizationsApi](/docs/generated/index.md#organizationsapi) — Manage organizations
- [ProjectsApi](/docs/generated/index.md#projectsapi) — Manage projects
- [SecretsApi](/docs/generated/index.md#secretsapi) — Manage secrets
- [ServiceOverridesApi](/docs/generated/index.md#serviceoverridesapi) — Manage service_overrides
- [ServicesApi](/docs/generated/index.md#servicesapi) — Manage services
- [UserGroupsApi](/docs/generated/index.md#usergroupsapi) — Manage user_groups
- [VariablesApi](/docs/generated/index.md#variablesapi) — Manage variables

#### Authorization (AuthZ)

- [ResourceGroupsApi](/docs/generated/index.md#resourcegroupsapi) — Manage resource_groups
- [RoleAssignmentsApi](/docs/generated/index.md#roleassignmentsapi) — Manage role_assignments
- [RolesApi](/docs/generated/index.md#rolesapi) — Manage roles

#### Pipeline Execution

- [InputSetsV0Api](/docs/generated/index.md#inputsetsv0api) — Manage input_sets_v0
- [PipelinesV0Api](/docs/generated/index.md#pipelinesv0api) — Manage pipelines_v0
- [TriggersV0Api](/docs/generated/index.md#triggersv0api) — Manage triggers_v0

#### Infrastructure as Code (IACM)

- [WorkspaceApprovalsApi](/docs/generated/index.md#workspaceapprovalsapi) — Manage workspace_approvals
- [WorkspaceDefaultPipelinesApi](/docs/generated/index.md#workspacedefaultpipelinesapi) — Manage workspace_default_pipelines
- [WorkspaceStatesApi](/docs/generated/index.md#workspacestatesapi) — Manage workspace_states
- [WorkspaceVariablesApi](/docs/generated/index.md#workspacevariablesapi) — Manage workspace_variables
- [WorkspacesApi](/docs/generated/index.md#workspacesapi) — Manage workspaces

#### Internal Developer Portal (IDP)

- [CatalogCustomPropertiesApi](/docs/generated/index.md#catalogcustompropertiesapi) — Manage catalog_custom_properties
- [EntitiesApi](/docs/generated/index.md#entitiesapi) — Manage entities
- [ScoresApi](/docs/generated/index.md#scoresapi) — Manage scores

#### Templates

- [TemplatesV0Api](/docs/generated/index.md#templatesv0api) — Manage templates_v0

## Error Handling

### Exception Types
- [HarnessSdkError](/docs/generated/index.md#harnessdkerror) — Base exception
- [ScopeNotSetError](/docs/generated/index.md#scopenotset) — Missing scope error
- [ApiError](/docs/generated/index.md#apierror) — API error (non-auth)
- [AuthError](/docs/generated/index.md#autherror) — Authentication/authorization error

### Common Error Scenarios
- 401/403 Authentication failures — Raises `AuthError`
- 404 Not found — Returns empty dict or False (doesn't raise)
- 429/503 Rate limit/service unavailable — Auto-retries with exponential backoff
- 400/500 Other errors — Raises `ApiError` with status/body/headers

## Pagination

- [Offset Pagination](/docs/generated/index.md#offset-pagination) — Page index + size
- [Cursor Pagination](/docs/generated/index.md#cursor-pagination) — Token-based pagination

## Authentication

- API Key based (x-api-key header)
- Account ID required (x-account-id header)
- Optional Organization/Project scope

## Examples

### Initialize Client
```python
from harness_platform_sdk import HarnessClient

client = HarnessClient(
    api_key="YOUR_API_KEY",
    account_id="YOUR_ACCOUNT_ID"
)
```

### List Organizations
```python
orgs = client.organizations.list()
for org in orgs:
    print(f"{org.get('identifier')}: {org.get('name')}")
```

### Get Organization with Scope
```python
from harness_platform_sdk import Scope

scope = Scope(account_id="MY_ACCOUNT", org="MY_ORG")
org = client.organizations.get(
    org_id="MY_ORG",
    scope=scope
)
```

### Handle Errors
```python
from harness_platform_sdk import (
    HarnessClient,
    ApiError,
    AuthError,
    ScopeNotSetError
)

try:
    client = HarnessClient(api_key="KEY", account_id="ACCT")
    org = client.organizations.get("org_id")
except AuthError as e:
    print(f"Auth failed: {e.status_code}")
except ApiError as e:
    print(f"API error: {e.status_code}, {e.body}")
except ScopeNotSetError as e:
    print(f"Scope error: {e}")
```

## Configuration

- `api_key` (required) — API key for authentication
- `account_id` (required) — Harness account ID
- `base_url` (optional) — API base URL, defaults to https://app.harness.io
- `timeout` (optional) — Request timeout in seconds, defaults to 30
- `max_retries` (optional) — Max retry attempts, defaults to 3
- `retry_status_codes` (optional) — HTTP codes to retry, defaults to [429, 503]
- `retry_enabled` (optional) — Enable retry, defaults to True
- `verify_ssl` (optional) — Verify SSL certificates, defaults to True

## Type Hints

All public API methods include full type hints:
- Parameter types documented
- Return types documented
- Exception types documented
- Compatible with type checkers (mypy, pyright)

See `py.typed` marker in package for PEP 561 compliance.

## Testing

```bash
# Run tests
python -m pytest tests/ -v

# Check type hints
mypy src/harness_platform_sdk

# Lint docstrings
ruff check --select D src/harness_platform_sdk
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Development setup
- Docstring style requirements
- Type hint expectations
- Testing guidelines

## License

BUSL-1.1 (Business Source License)

## Links

- [GitHub Repository](https://github.com/anthropics/harness-platform-sdk)
- [Python Package Index (PyPI)](https://pypi.org/project/harness-platform-sdk/)
- [Harness Platform Documentation](https://docs.harness.io/)