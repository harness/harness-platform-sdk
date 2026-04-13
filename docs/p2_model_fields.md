# P2 Domain Model Fields Specification

This document defines the request/response schemas and endpoint paths for all P2 domains
in the Harness Python SDK. This is the source of truth for T2/T3/T4 model and API
implementation.

> **How to use this doc:**
> Each domain section has an **Envelope Contract** table that must be completed before
> any API file is authored. All three rows are required — leave none blank. The
> integration test mocks must match the shapes in that table exactly.

---

## Envelope Contract (per-domain — complete before authoring)

Every domain section contains this table. Fill it in during field research (T1 of any
domain spec) by inspecting `openapi/harness-openapi-normalized.yaml`:

| Row | Question | Example values |
|---|---|---|
| **List envelope** | Shape of `list()` response body | `data.content[]` / `direct array` / `data.{resource}[]` |
| **Singleton envelope** | Shape of `get()` / `create()` / `update()` response body | `data.{resource} + siblings` / `flat data.{...}` |
| **Request body wrapper** | Shape of `create()` / `update()` request body | `{"resource": {...}}` / flat `{...}` |
| **unwrap_field (list)** | Value passed to `_paginate(unwrap_field=...)` | `"connector"` / `None` |
| **unwrap_field (singleton)** | Key to extract from `data` dict before model construction | `"organization"` / `None` |

> **Canonical examples:**
> - Named-wrapper pattern (Organizations, Projects): `api/organizations.py`, `api/projects.py`
> - Array-unwrap pattern (Connectors, Secrets, Infrastructure): `api/connectors.py`
> - Direct array pattern (Pipelines): `api/pipelines.py`

---

## Organizations

**Scope:** Account-scoped only
**x-tagGroup:** `organizations`

**Endpoints:**

| Method | Path |
|---|---|
| list | `GET /ng/api/organizations` |
| get | `GET /ng/api/organizations/{identifier}` |
| create | `POST /ng/api/organizations` |
| update | `PUT /ng/api/organizations/{identifier}` |
| delete | `DELETE /ng/api/organizations/{identifier}` |

**Envelope Contract:**

| Row | Value |
|---|---|
| List envelope | `data.content[]` — each item is `{"organization": {...}, "createdAt": ..., "lastModifiedAt": ..., "harnessManaged": ...}` |
| Singleton envelope | `data.organization` (core fields) + `data.createdAt`, `data.lastModifiedAt`, `data.harnessManaged` as siblings |
| Request body wrapper | `{"organization": {"identifier": ..., "name": ..., ...}}` |
| unwrap_field (list) | `"organization"` |
| unwrap_field (singleton) | `"organization"` — merge with siblings before constructing `OrganizationResponse` |

**Pagination:** OFFSET (`pageIndex` / `pageSize`)

### OrganizationResponse fields

| Python attr | Alias (camelCase) | Type | Required | Source in envelope |
|---|---|---|---|---|
| identifier | identifier | str | yes | `data.organization.identifier` |
| name | name | str | yes | `data.organization.name` |
| description | description | str | no | `data.organization.description` |
| tags | tags | dict[str, str] | no | `data.organization.tags` |
| harness_managed | harnessManaged | bool | no | `data.harnessManaged` (sibling) |
| created | createdAt | int | no | `data.createdAt` (sibling) |
| updated | lastModifiedAt | int | no | `data.lastModifiedAt` (sibling) |

### OrganizationCreateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

### OrganizationUpdateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

---

## Projects

**Scope:** Organization-scoped (org required in path)
**x-tagGroup:** `projects`

**Endpoints:**

| Method | Path |
|---|---|
| list | `GET /v1/orgs/{org}/projects` |
| get | `GET /v1/orgs/{org}/projects/{project_id}` |
| create | `POST /v1/orgs/{org}/projects` |
| update | `PUT /v1/orgs/{org}/projects/{project_id}` |
| delete | `DELETE /v1/orgs/{org}/projects/{project_id}` |

**Envelope Contract:**

| Row | Value |
|---|---|
| List envelope | `data.content[]` — each item is `{"project": {...}, "created": ..., "updated": ..., "isFavorite": ...}` |
| Singleton envelope | `data.project` (core fields) + `data.created`, `data.updated`, `data.isFavorite` as siblings |
| Request body wrapper | `{"project": {"identifier": ..., "name": ..., ...}}` |
| unwrap_field (list) | `"project"` |
| unwrap_field (singleton) | `"project"` — merge with siblings before constructing `ProjectResponse` |

**Pagination:** OFFSET (`pageIndex` / `pageSize`)

### ProjectResponse fields

| Python attr | Alias (camelCase) | Type | Required | Source in envelope |
|---|---|---|---|---|
| identifier | identifier | str | yes | `data.project.identifier` |
| name | name | str | yes | `data.project.name` |
| org | org | str | yes | `data.project.org` |
| description | description | str | no | `data.project.description` |
| tags | tags | dict[str, str] | no | `data.project.tags` |
| is_favorite | isFavorite | bool | yes | `data.isFavorite` (sibling) |
| created | created | int | no | `data.created` (sibling) |
| updated | updated | int | no | `data.updated` (sibling) |

### ProjectCreateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

### ProjectUpdateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

---

## Services

**Scope:** Project-scoped (org + project required in path)
**x-tagGroup:** `services`

**Endpoints:**

| Method | Path |
|---|---|
| list | `GET /v1/orgs/{org}/projects/{project}/services` |
| get | `GET /v1/orgs/{org}/projects/{project}/services/{service_id}` |
| create | `POST /v1/orgs/{org}/projects/{project}/services` |
| update | `PUT /v1/orgs/{org}/projects/{project}/services/{service_id}` |
| delete | `DELETE /v1/orgs/{org}/projects/{project}/services/{service_id}` |

**Envelope Contract:**

| Row | Value |
|---|---|
| List envelope | `data.content[]` — direct array of wrapped items |
| Singleton envelope | `data.service` (core fields) + metadata siblings (`created`, `updated`) |
| Request body wrapper | `{"service": {"identifier": ..., "name": ..., ...}}` — confirmed wrapped — spec-inspected (v3e) |
| unwrap_field (list) | `"service"` |
| unwrap_field (singleton) | `"service"` — merge with siblings before constructing `ServiceResponse` |

**Pagination:** OFFSET (`pageIndex` / `pageSize`)

### ServiceResponse fields

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | |
| name | name | str | yes | |
| org | org | str | yes | |
| project | project | str | yes | |
| description | description | str | no | |
| tags | tags | dict[str, str] | no | |
| service_yaml | serviceYaml | str | no | Full YAML definition |
| created | created | int | no | |
| updated | updated | int | no | |

### ServiceCreateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| service_yaml | serviceYaml | str | no |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

### ServiceUpdateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| service_yaml | serviceYaml | str | no |
| description | description | str | no |
| tags | tags | dict[str, str] | no |

---

## Roles

**Scope:** Organization-scoped (org required, NOT project-scoped)
**x-tagGroup:** `roles`

**Endpoints:**

| Method | Path |
|---|---|
| list | `GET /v1/orgs/{org}/roles` |
| get | `GET /v1/orgs/{org}/roles/{role_id}` |
| create | `POST /v1/orgs/{org}/roles` |
| update | `PUT /v1/orgs/{org}/roles/{role_id}` |
| delete | `DELETE /v1/orgs/{org}/roles/{role_id}` |

**Envelope Contract:**

| Row | Value |
|---|---|
| List envelope | `data.content[]` — confirmed flat — spec-inspected (v3e) |
| Singleton envelope | Flat `RoleResponse` object (all properties directly) — confirmed flat — spec-inspected (v3e) |
| Request body wrapper | Flat `{"identifier": ..., "name": ..., ...}` — confirmed flat — spec-inspected (v3e) |
| unwrap_field (list) | `None` |
| unwrap_field (singleton) | `None` |

**Pagination:** OFFSET (`pageIndex` / `pageSize`)

### RoleResponse fields

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | |
| name | name | str | yes | |
| description | description | str | no | |
| allowed_scope_levels | allowedScopeLevels | list[str] | yes | ACCOUNT, ORG, PROJECT |
| permissions | permissions | list[str] | no | |
| created | created | int | no | |
| updated | updated | int | no | |

### RoleCreateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| allowed_scope_levels | allowedScopeLevels | list[str] | yes |
| description | description | str | no |
| permissions | permissions | list[str] | no |

### RoleUpdateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| description | description | str | no |
| permissions | permissions | list[str] | no |

---

## Resource Groups

**Scope:** Organization-scoped (org required, NOT project-scoped)
**x-tagGroup:** `resource-groups`

**Endpoints:**

| Method | Path |
|---|---|
| list | `GET /v1/orgs/{org}/resource-groups` |
| get | `GET /v1/orgs/{org}/resource-groups/{resource_group_id}` |
| create | `POST /v1/orgs/{org}/resource-groups` |
| update | `PUT /v1/orgs/{org}/resource-groups/{resource_group_id}` |
| delete | `DELETE /v1/orgs/{org}/resource-groups/{resource_group_id}` |

**Envelope Contract:**

| Row | Value |
|---|---|
| List envelope | `data.content[]` — direct array of wrapped items |
| Singleton envelope | `data.resourceGroup` (core fields) + metadata siblings (`createdAt`, `lastModifiedAt`, `harnessManaged`) |
| Request body wrapper | `{"resourceGroup": {"identifier": ..., "name": ..., ...}}` — confirmed wrapped — spec-inspected (v3e) |
| unwrap_field (list) | `"resourceGroup"` |
| unwrap_field (singleton) | `"resourceGroup"` — merge with siblings before constructing `ResourceGroupResponse` |

**Pagination:** OFFSET (`pageIndex` / `pageSize`)

### ResourceGroupResponse fields

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | |
| name | name | str | yes | |
| description | description | str | no | |
| resource_filter | resourceFilter | dict | no | Resource filtering criteria |
| created | created | int | no | |
| updated | updated | int | no | |

### ResourceGroupCreateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| resource_filter | resourceFilter | dict | no |
| description | description | str | no |

### ResourceGroupUpdateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| identifier | identifier | str | yes |
| name | name | str | yes |
| resource_filter | resourceFilter | dict | no |
| description | description | str | no |

---

## Role Assignments

**Scope:** Organization-scoped (org required, NOT project-scoped)
**x-tagGroup:** `role-assignments`

**Endpoints:**

| Method | Path |
|---|---|
| list | `GET /v1/orgs/{org}/role-assignments` |
| get | `GET /v1/orgs/{org}/role-assignments/{role_assignment_id}` |
| create | `POST /v1/orgs/{org}/role-assignments` (maps to `bulkCreate` with single item) |
| update | NOT AVAILABLE — use delete + create |
| delete | `DELETE /v1/orgs/{org}/role-assignments/{role_assignment_id}` |

**Envelope Contract:**

| Row | Value |
|---|---|
| List envelope | `data.content[]` — direct array of wrapped items |
| Singleton envelope | `data.role-assignment` (core fields) + metadata siblings (`created`, `updated`, `harness_managed`) |
| Request body wrapper | `{"role-assignment": {"roleIdentifier": ..., "scope": ..., "principal": ...}}` — confirmed wrapped — spec-inspected (v3e) |
| unwrap_field (list) | `"role-assignment"` |
| unwrap_field (singleton) | `"role-assignment"` — merge with siblings before constructing `RoleAssignmentResponse` |

**Pagination:** OFFSET (`pageIndex` / `pageSize`)

**Note:** No `update()` endpoint exists. Pattern is delete + create. SDK `update()` method should raise `NotImplementedError`.

### RoleAssignmentResponse fields

| Python attr | Alias (camelCase) | Type | Required | Notes |
|---|---|---|---|---|
| identifier | identifier | str | yes | |
| role_identifier | roleIdentifier | str | yes | |
| scope | scope | dict | yes | `{scopeType, scopeId}` |
| principal | principal | dict | yes | `{type: USER/SERVICE_ACCOUNT, identifier}` |
| disabled | disabled | bool | no | |
| created | created | int | no | |
| updated | updated | int | no | |

### RoleAssignmentCreateRequest fields

| Python attr | Alias (camelCase) | Type | Required |
|---|---|---|---|
| role_identifier | roleIdentifier | str | yes |
| scope | scope | dict | yes |
| principal | principal | dict | yes |
| disabled | disabled | bool | no |

---

## Pagination Reference

All P2 list endpoints use `PageResponse` wrapper:

| Field | Type | Notes |
|---|---|---|
| pageIndex | int | 0-based page number |
| pageSize | int | Items per page (max 100) |
| pageItemCount | int | Items on current page — use to detect end when `< pageSize` |
| totalItems | int | Total count of all items |
| totalPages | int | Total page count |
| content | list | Domain objects (wrapped or flat per domain's envelope contract) |

**Pagination style:** OFFSET for all P2 domains.

---

## Field Research Checklist (T1 of any domain spec)

Use this checklist when authoring `docs/p{n}_model_fields.md` for any new domain batch.
All items must be answered from `openapi/harness-openapi-normalized.yaml` inspection —
never assumed.

```
For each domain:
[ ] x-tagGroup name (exact string from spec)
[ ] URL path templates for list, get, create, update, delete
[ ] Scope level: account-only / account+org / account+org+project
[ ] List envelope shape (what does the list response body look like?)
[ ] Singleton envelope shape (what does get/create/update response body look like?)
[ ] Request body wrapper (is the body flat or wrapped under a named key?)
[ ] unwrap_field (list): value or None
[ ] unwrap_field (singleton): value or None, plus merge strategy if siblings present
[ ] Pagination style: OFFSET / CURSOR / UNKNOWN
[ ] Response model fields (name, alias, type, required)
[ ] CreateRequest fields (or note "raw dict" if <3 fields and no required)
[ ] UpdateRequest fields (or note "not available" if no PUT endpoint)
```

**Verify command for the completed doc:**
```bash
# All domains have an Envelope Contract table (5 required rows)
grep -c "unwrap_field (singleton)" docs/p{n}_model_fields.md
# Must equal the number of domains in this batch

# All domains have singleton envelope documented
grep -c "Singleton envelope" docs/p{n}_model_fields.md
# Must equal the number of domains in this batch

# All domains have request body wrapper documented
grep -c "Request body wrapper" docs/p{n}_model_fields.md
# Must equal the number of domains in this batch
```

---

## API File Verify Checklist (T2+ of any domain spec)

Add these checks to the Verify block of every domain API file task:

```bash
# Confirm request body wrapping is present if domain uses named wrapper
# (skip this check if Request body wrapper = flat in the Envelope Contract)
grep -A 5 "def create" src/harness_python_sdk/api/{domain}.py | grep '"{resource_key}"'

# Confirm singleton get() unwraps if domain uses named wrapper
grep -A 15 "def get" src/harness_python_sdk/api/{domain}.py | grep 'unwrap\|{resource_key}'

# Confirm _paginate() passes correct unwrap_field
grep "_paginate" src/harness_python_sdk/api/{domain}.py | grep 'unwrap_field'
```

---

## ResponseDTO Outer Wrapper (all domains)

All Harness API responses share this outer envelope — handled by `_get()`, `_post()`, `_put()`, `_delete()` in `client.py`:

```yaml
status: "SUCCESS" | "FAILURE"
data: <domain-specific shape — see Envelope Contract per domain>
metaData: object
correlationId: string
```

The `data` key is what the domain API methods receive. The Envelope Contract table above describes what `data` contains per domain.
