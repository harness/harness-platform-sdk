# Harness Platform SDK - Docker Repository Overview

## Description

Production-grade Python Docker image for the Harness Platform SDK — a fully-typed API client for Harness platform resources. Built with Pydantic v2, httpx, and enterprise-grade retry logic for reliable platform interactions.

---

## Quick Start

```bash
# Pull the latest image
docker pull harnesssolutionfactory/harness-platform-sdk:latest

# Run Python with the SDK
docker run --rm harnesssolutionfactory/harness-platform-sdk:latest -c "from harness_platform_sdk import HarnessClient; print('SDK ready')"

# Use a mounted script
docker run --rm -v $(pwd)/script.py:/app/script.py harnesssolutionfactory/harness-platform-sdk:latest /app/script.py
```

## What's Included

- **Python 3.11+** runtime with Alpine base
- **Harness Platform SDK v1.0.0** — production-ready Python library
- **Pre-installed dependencies:**
  - httpx (async-capable HTTP client)
  - Pydantic v2 (data validation)
  - tenacity (retry orchestration)
  - PyYAML (configuration parsing)
- **Virtual environment** (/opt/venv) — no package conflicts
- **SSL X.509 strict mode** — enterprise security

---

## Supported Resource APIs

The SDK provides typed access to:

- **Next-Gen:** Organizations, Projects, Services, Connectors, Secrets, Environments
- **Pipeline:** Pipelines, Input Sets, Triggers, Templates
- **Authorization:** Roles, Resource Groups, Role Assignments
- **IaC:** Workspaces, Workspace Variables, Workspace Approvals
- **Internal Developer Portal:** Entities, Catalog Properties, Scores

---

## Key Features

✅ **Single Entry Point** — All APIs via `HarnessClient`
✅ **Automatic Retry** — Built-in retry on 429 (rate limit) and 503 (service unavailable) with exponential backoff
✅ **Scope Resolution** — Automatic account/org/project context merging
✅ **Type Safety** — Full Pydantic v2 validation
✅ **Error Handling** — Explicit exception hierarchy (AuthError, ApiError, ScopeNotSetError)
✅ **Pagination Support** — OFFSET and CURSOR-based pagination

---

## Usage Example

```python
from harness_platform_sdk import HarnessClient

# Initialize client
client = HarnessClient(
    api_key="your-api-key",
    account_id="your-account-id",
    default_org="your-org",
    default_project="your-project"
)

# Use context manager for automatic cleanup
with client:
    orgs = client.organizations.list()
    for org in orgs:
        print(f"Organization: {org.identifier}")
```

---

## Configuration

The SDK accepts configuration via:

1. **Environment Variables**
   - `HARNESS_API_KEY` — API key for authentication
   - `HARNESS_ACCOUNT_ID` — Account identifier
   - `HARNESS_BASE_URL` — Platform URL (default: https://app.harness.io)

2. **Constructor Arguments**
   ```python
   HarnessClient(
       api_key="key",
       account_id="acc",
       default_org="org",
       default_project="proj",
       base_url="https://app.harness.io",
       timeout=30.0,
       max_retries=3,
       retry_enabled=True,
       verify_ssl=True
   )
   ```

3. **HarnessConfig Object**
   ```python
   from harness_platform_sdk import HarnessConfig, HarnessClient

   config = HarnessConfig(api_key="...", account_id="...")
   client = HarnessClient(config=config)
   ```

---

## Error Handling

The SDK provides explicit error types:

- **AuthError** — 401/403 authentication failures
- **ApiError** — Non-2xx API responses (includes status, body, headers)
- **ScopeNotSetError** — Missing required scope fields
- **HarnessSdkError** — Base exception for all SDK errors

---

## Security

- **Non-root user** (UID 1000) by default
- **SSL X.509 strict mode** enabled (`SSL_VERIFY_X509_STRICT=true`)
- **BUSL-1.1 licensed** — See License for terms
- **Built with minimal attack surface** — Alpine Linux base

---

## Python Version

- **Minimum:** Python 3.11
- **Tested:** Python 3.11, 3.12
- **Recommended:** Python 3.12+

---

## Links

- **Documentation:** https://developer.harness.io/harness-solutions-factory/use-hsf/plugins/harness-platform-sdk
- **Repository:** https://github.com/harness/harness-platform-sdk
- **Issues:** https://github.com/harness/harness-platform-sdk/issues
- **License:** BUSL-1.1

---

## Versioning

Image tags follow `harness-platform-sdk:<version>`, corresponding to PyPI releases. Each image is tagged with:
- Version (e.g., `1.0.0`)
- Git SHA (e.g., `sha-a1b2c3d`)
- `latest` (current stable)

---

## Support

For issues, documentation, or questions:
- **GitHub Issues:** https://github.com/harness/harness-platform-sdk/issues
- **Documentation:** https://developer.harness.io/harness-solutions-factory/use-hsf/plugins/harness-platform-sdk
- **AI-Agent Docs:** https://developer.harness.io/harness-solutions-factory/use-hsf/plugins/harness-platform-sdk/llms.md
- **Email:** platform@harness.io

---

**Maintained by:** Harness
**License:** BUSL-1.1
**Last Updated:** 2026-09-21
