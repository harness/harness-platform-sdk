# P1 Integration Test Reference

## Pipelines

| Method | URL (with test-org/test-project substituted) | Pagination |
|---|---|---|
| list   | /v1/orgs/test-org/projects/test-project/pipelines | OFFSET |
| get    | /v1/orgs/test-org/projects/test-project/pipelines/{pipeline_id} | — |
| create | /v1/orgs/test-org/projects/test-project/pipelines | — |

### PipelineResponse minimal mock payload
```json
{
  "identifier": "pipeline-1",
  "name": "Test Pipeline"
}
```

### PipelineCreateRequest minimal valid payload
```json
{
  "identifier": "pipeline-1",
  "name": "Test Pipeline",
  "pipelineYaml": "pipeline:\n  name: Test\n"
}
```

---

## Connectors

| Method | URL (with test-org/test-project substituted) | Pagination |
|---|---|---|
| list   | /ng/api/connectors | OFFSET |
| get    | /ng/api/connectors/{identifier} | — |
| create | /ng/api/connectors | — |

### ConnectorResponse minimal mock payload
```json
{
  "identifier": "connector-1",
  "name": "Test Connector"
}
```

### ConnectorCreateRequest minimal valid payload
```json
{
  "identifier": "connector-1",
  "name": "Test Connector",
  "spec": {}
}
```

**Note:** `list()` uses `unwrap_field="connector"` — each item in the `content` array is wrapped as `{"connector": {...}}`.

---

## Secrets

| Method | URL (with test-org/test-project substituted) | Pagination |
|---|---|---|
| list   | /ng/api/v2/secrets | OFFSET |
| get    | /ng/api/v2/secrets/{identifier} | — |
| create | /ng/api/v2/secrets | — |

### SecretResponse minimal mock payload
```json
{
  "identifier": "secret-1",
  "name": "Test Secret"
}
```

### SecretCreateRequest minimal valid payload
```json
{
  "identifier": "secret-1",
  "name": "Test Secret",
  "spec": {}
}
```

**Note:** `list()` uses `unwrap_field="secret"` — each item in the `content` array is wrapped as `{"secret": {...}}`.

---

## Infrastructure

| Method | URL (with test-org/test-project substituted) | Pagination |
|---|---|---|
| list   | /ng/api/infrastructures | OFFSET |
| get    | /ng/api/infrastructures/{infraIdentifier} | — |
| create | /ng/api/infrastructures | — |

### InfrastructureResponse minimal mock payload
```json
{
  "identifier": "infra-1",
  "name": "Test Infrastructure",
  "type": "KubernetesDirect",
  "environment": "env-1"
}
```

### InfrastructureCreateRequest minimal valid payload
```json
{
  "identifier": "infra-1",
  "name": "Test Infrastructure",
  "type": "KubernetesDirect",
  "environment": "env-1"
}
```

**Note:** `list()` uses `unwrap_field="infrastructure"` — each item in the `content` array is wrapped as `{"infrastructure": {...}}`.

---

## Pagination Pattern (OFFSET)

All P1 domains use OFFSET pagination with the following response envelope:
```json
{
  "content": [
    { /* item 1 */ },
    { /* item 2 */ }
  ],
  "pageIndex": 0,
  "pageSize": 10,
  "totalPages": 2
}
```

**End signal:** `pageIndex + 1 >= totalPages` or `content` is empty.

For multi-page tests:
- Page 1: `pageIndex: 0, pageSize: 10, totalPages: 2` (signals 2 pages total)
- Page 2: `pageIndex: 1, pageSize: 10, totalPages: 2` (final page)
