# P1 Domain Model Fields Specification

This document defines the request/response schemas and endpoint paths for all P1 domains in the Harness Python SDK. This is the source of truth for T2 model implementation.

---

## Pipelines

**list:** GET /v1/orgs/{org}/projects/{project}/pipelines — OFFSET
**get:** GET /v1/orgs/{org}/projects/{project}/pipelines/{pipeline_id}
**create:** POST /v1/orgs/{org}/projects/{project}/pipelines
**update:** PUT /v1/orgs/{org}/projects/{project}/pipelines/{pipeline_id}
**delete:** DELETE /v1/orgs/{org}/projects/{project}/pipelines/{pipeline_id}

### PipelineResponse fields

Used for both `list()` item response and `get()` response.

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | Pipeline unique identifier |
| name | name | str | yes | Human-readable pipeline name |
| org | org | str | no | Organization identifier |
| project | project | str | no | Project identifier |
| description | description | str | no | Pipeline description |
| tags | tags | dict[str, str] | no | Key-value tags |
| modules | modules | list[str] | no | Harness modules (CD, CI, CV, etc) |
| created | created | int | no | Creation timestamp (ms) |
| updated | updated | int | no | Last update timestamp (ms) |
| pipeline_yaml | pipelineYaml | str | no | Pipeline YAML definition |
| template_applied_pipeline_yaml | templateAppliedPipelineYaml | str | no | Pipeline YAML with templates applied |
| git_details | gitDetails | dict | no | Git sync metadata |
| valid | valid | bool | no | Whether pipeline YAML is valid |
| connector_ref | connectorRef | str | no | Git connector reference |
| store_type | storeType | str | no | Where pipeline is stored (INLINE, REMOTE) |
| yaml_version | yamlVersion | str | no | YAML schema version |

### PipelineCreateRequest fields

Used for `create()` method. Subset of fields required for creation.

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| pipeline_yaml | pipelineYaml | str | yes |
| org | org | str | no |
| project | project | str | no |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

### PipelineUpdateRequest fields

Used for `update()` method. Updatable fields from response.

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| pipeline_yaml | pipelineYaml | str | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

---

## Connectors

**list:** GET /ng/api/connectors — OFFSET (via pageIndex/pageSize params)
**get:** GET /ng/api/connectors/{identifier}
**create:** POST /ng/api/connectors
**update:** PUT /ng/api/connectors/{identifier} — NOT YET AVAILABLE IN SPEC (will implement DELETE + CREATE pattern)
**delete:** DELETE /ng/api/connectors/{identifier}

### ConnectorResponse fields

Used for both `list()` item response and `get()` response.

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | Connector unique identifier |
| name | name | str | yes | Human-readable connector name |
| org | org | str | no | Organization identifier |
| project | project | str | no | Project identifier |
| description | description | str | no | Connector description |
| tags | tags | dict[str, str] | no | Key-value tags |
| created | created | int | no | Creation timestamp (ms) |
| updated | updated | int | no | Last update timestamp (ms) |
| spec | spec | dict | no | Connector-specific configuration (polymorphic) |
| status | status | dict | no | Connector connectivity details |
| harness_managed | harnessManagedConnector | bool | no | Whether Harness manages this connector |
| governance_metadata | governanceMetadata | dict | no | Governance policy metadata |

### ConnectorCreateRequest fields

Used for `create()` method.

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| spec | spec | dict | yes |
| org | org | str | no |
| project | project | str | no |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

### ConnectorUpdateRequest fields

Used for `update()` method (DELETE + CREATE pattern).

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| spec | spec | dict | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

---

## Secrets

**list:** GET /ng/api/v2/secrets — OFFSET (via pageIndex/pageSize params)
**get:** GET /ng/api/v2/secrets/{identifier}
**create:** POST /ng/api/v2/secrets
**update:** PUT /ng/api/v2/secrets/{identifier}
**delete:** DELETE /ng/api/v2/secrets/{identifier}

### SecretResponse fields

Used for both `list()` item response and `get()` response.

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | Secret unique identifier |
| name | name | str | yes | Human-readable secret name |
| org | org | str | no | Organization identifier |
| project | project | str | no | Project identifier |
| description | description | str | no | Secret description |
| tags | tags | dict[str, str] | no | Key-value tags |
| created | created | int | no | Creation timestamp (ms) |
| updated | updated | int | no | Last update timestamp (ms) |
| spec | spec | dict | no | Secret-specific configuration (polymorphic) |
| draft | draft | bool | no | Whether this is a draft |
| governance_metadata | governanceMetadata | dict | no | Governance policy metadata |

### SecretCreateRequest fields

Used for `create()` method.

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| spec | spec | dict | yes |
| org | org | str | no |
| project | project | str | no |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

### SecretUpdateRequest fields

Used for `update()` method.

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| spec | spec | dict | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

---

## Infrastructure

**list:** GET /ng/api/infrastructures — OFFSET (via page/size params, note: different param names!)
**get:** GET /ng/api/infrastructures/{infraIdentifier}
**create:** POST /ng/api/infrastructures
**update:** PUT /ng/api/infrastructures/{infraIdentifier} — NOT YET AVAILABLE IN SPEC (will implement DELETE + CREATE pattern)
**delete:** DELETE /ng/api/infrastructures/{infraIdentifier}

### InfrastructureResponse fields

Used for both `list()` item response and `get()` response.

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | Infrastructure unique identifier |
| name | name | str | yes | Human-readable infrastructure name |
| org | org | str | no | Organization identifier |
| project | project | str | no | Project identifier |
| account | account | str | no | Account identifier |
| environment | environment | str | no | Environment identifier (required for scoping) |
| type | type | str | yes | Infrastructure type (Kubernetes, SSH, WinRm, etc) |
| description | description | str | no | Infrastructure description |
| tags | tags | dict[str, str] | no | Key-value tags |
| created | created | int | no | Creation timestamp (ms) |
| updated | updated | int | no | Last update timestamp (ms) |
| harness_version | harnessVersion | str | no | Harness infrastructure version |
| yaml | yaml | str | no | Infrastructure YAML definition |

### InfrastructureCreateRequest fields

Used for `create()` method.

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| type | type | str | yes |
| environment | environment | str | yes |
| org | org | str | no |
| project | project | str | no |
| description | description | str | no |
| tags | tags | dict[str, str] | no |
| yaml | yaml | str | no |

### InfrastructureUpdateRequest fields

Used for `update()` method (DELETE + CREATE pattern).

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| type | type | str | yes |
| environment | environment | str | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |
| yaml | yaml | str | no |

---

## Pagination Notes

- **Pipelines**: Uses standard `pageIndex` / `pageSize` (OFFSET style)
- **Connectors**: Uses `pageIndex` / `pageSize` (OFFSET style)
- **Secrets**: Uses `pageIndex` / `pageSize` (OFFSET style)
- **Infrastructure**: Uses `page` / `size` (note different param names, but still OFFSET style)

All list endpoints should auto-paginate internally. The `_paginate()` method on `HarnessClient` handles this.

---

## Implementation Notes

1. All fields use snake_case in Python; camelCase aliases map via `Field(alias=...)`
2. Optional fields should use `X | None` syntax (Pydantic v2)
3. Dict fields (`spec`, `tags`, `governance_metadata`, `status`) are left as plain `dict` unless  strongly typed later
4. All models inherit from `HarnessModel` (which sets `extra="allow"` and `populate_by_name=True`)
5. No UPDATE endpoint exists for Connectors and Infrastructure in current spec; handle via DELETE + CREATE pattern
6. Timestamp fields (`created`, `updated`) are integers (milliseconds since epoch)
