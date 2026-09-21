# Harness Platform SDK v1.0.0

**Release Date:** September 14, 2026

**Status:** **Production Ready**

---

## Overview

Harness Platform SDK v1.0.0 is the first stable production release of the newly-branded **harness-platform-sdk** — a comprehensive Python SDK for the entire Harness platform API ecosystem.

This release culminates the rebranding and feature development from the previous `harness-python-sdk` package, expanding the SDK's scope to cover all major Harness platform domains: Next-Gen, Pipelines, Authorization, Infrastructure-as-Code, and Internal Developer Portal.

**Python Support:** 3.11+ (tested on 3.11, 3.12, 3.14)

**Full Changelog**: https://github.com/harness/harness-platform-sdk/compare/v0.13.0...v1.0.0
---

## Major Features

### Production-Ready API Coverage

- **Next-Gen (Core):** Organizations, Projects, Services, Service Overrides, Connectors, Secrets, Infrastructures, Variables, User Groups, Environments V2
- **Pipelines:** Pipelines (v0), Input Sets (v0), Triggers (v0), Templates (v0)
- **Authorization:** Roles, Resource Groups, Role Assignments
- **Infrastructure-as-Code (IaC):** Workspaces, Workspace Approvals, Workspace States, Workspace Variables, Workspace Default Pipelines
- **Internal Developer Portal (IDP):** Entities, Catalog Custom Properties, Scores

### Core Capabilities

✅ **Single Entry Point** — All domain APIs via unified `HarnessClient`
✅ **Automatic Retry Logic** — Built-in exponential backoff on 429 (rate limit) and 503 (service unavailable)
✅ **Type Safety** — Full Pydantic v2 validation and IDE autocomplete
✅ **Scope Resolution** — Automatic account/org/project context merging
✅ **Flexible Pagination** — Support for both OFFSET and CURSOR-based pagination styles
✅ **Rich Error Hierarchy** — Explicit exception types (AuthError, ApiError, ScopeNotSetError)
✅ **Production Tested** — Comprehensive test coverage with unit and integration tests
✅ **Docker Ready** — Alpine-based container image with virtual environment isolation

---

## ⚠️ Breaking Changes

### Module Rename: `harness-python-sdk` → `harness-platform-sdk`

Users upgrading from v0.13.0 **must** update their code:

**Before (v0.13.0):**
```python
from harness_python_sdk import HarnessClient
```

**After (v1.0.0):**
```python
from harness_platform_sdk import HarnessClient
```

**Migration Steps:**

1. Update package dependency:
   ```bash
   pip uninstall harness-python-sdk
   pip install harness-platform-sdk>=1.0.0
   ```

2. Update all import statements across your codebase:
   ```bash
   grep -r "from harness_python_sdk" . --include="*.py"
   sed -i 's/from harness_python_sdk/from harness_platform_sdk/g' **/*.py
   ```

3. Test thoroughly in your environment

---

## What's New

### Package & Infrastructure

- **GitHub Actions PyPI Publish Workflow** — Automated trusted OIDC release pipeline
- **Complete API Documentation** — 76 generated markdown files covering all SDK modules
- **Documentation Build Tooling** — `mise build:docs` for markdown API reference generation
- **LLM-Friendly Documentation** — AI-Agent compatible docs via `llms.md`
- **Modular Lint Tasks** — Refined code quality workflow: `lint:black`, `lint:isort`, `lint:type-check`, `lint:docstrings`

### Developer Experience

- **Production Sample Scripts:**
  - `tests/sdk/list_pipelines.py` — Hierarchical pipeline discovery
  - `tests/sdk/list_workspaces.py` — Workspace filtering with smart matching
  - `tests/sdk/create_pipeline_from_template.py` — Pipeline creation from templates

- **Enhanced Documentation:**
  - `DOCSTRING_STYLE.md` — Google-style docstring guide
  - Updated `CONTRIBUTING.md` with Python Code Style section
  - Comprehensive module docstrings across all 71 API files

### Docker & Deployment

- **Production Docker Image** — Alpine Linux base with Python 3.14+
- **Multi-stage Build** — Optimized layers for reduced image size
- **Security Hardening** — CVE patches and non-root user execution
- **Virtual Environment Isolation** — `/opt/venv` for clean dependency management
- **SSL/TLS Configuration** — X.509 strict mode support with override capability

---

## Dependencies

### Core Dependencies
- **httpx** ≥0.25.0 — Modern async-capable HTTP client
- **pydantic** ≥2.0 — Data validation and serialization
- **tenacity** ≥8.2.0 — Retry orchestration
- **PyYAML** ==6.0.3 — Configuration file parsing

### Development Dependencies (Optional)
- pytest, pytest-httpx, pytest-cov — Testing framework
- mypy, ruff, black, isort — Code quality and formatting
- pdoc3 — API documentation generation
- Jinja2 — Template rendering

### Publishing Dependencies (Optional)
- build, twine, wheel — PyPI packaging and distribution

---

## Installation

### Via PyPI (Recommended)

```bash
pip install harness-platform-sdk>=1.0.0
```

### Via Docker

```bash
docker pull harnesssolutionfactory/harness-platform-sdk:1.0.0
docker run --rm harnesssolutionfactory/harness-platform-sdk:1.0.0 -c \
  "from harness_platform_sdk import HarnessClient; print('Ready')"
```

### From Source

```bash
git clone https://github.com/harness/harness-platform-sdk.git
cd harness-platform-sdk
pip install -e .
```

---

## Quick Example

```python
from harness_platform_sdk import HarnessClient, AuthError, ApiError

# Initialize client
client = HarnessClient(
    api_key="your-api-key",
    account_id="your-account-id",
    default_org="your-org",
    default_project="your-project"
)

# Use context manager for automatic cleanup
try:
    with client:
        # List organizations
        orgs = client.organizations.list()
        for org in orgs:
            print(f"Organization: {org.identifier}")

        # List projects in default org
        projects = client.projects.list()
        for project in projects:
            print(f"  Project: {project.name}")

        # Access pipelines with scope override
        pipelines = client.pipelines.list(org="other-org", project="other-project")
        for pipeline in pipelines:
            print(f"    Pipeline: {pipeline.identifier}")

except AuthError as e:
    print(f"Authentication failed: {e.status_code}")
except ApiError as e:
    print(f"API error: {e.status_code} - {e.body}")
```

---

## Security

- **BUSL-1.1 Licensed** — Proprietary open-source license with clear usage terms
- **Non-root Container** — Runs as UID 1000 by default
- **SSL X.509 Strict Mode** — Enterprise-grade certificate validation
- **Minimal Attack Surface** — Alpine Linux base reduces vulnerability footprint
- **Type-Safe Validation** — Pydantic v2 ensures data integrity at boundaries

---

## Documentation

- **Official Docs:** https://developer.harness.io/docs/harness-solutions-factory/plugins/harness-platform-sdk
- **API Reference:** https://developer.harness.io/docs/harness-solutions-factory/plugins/harness-platform-sdk/api-reference
- **AI-Agent Docs:** https://developer.harness.io/docs/harness-solutions-factory/plugins/harness-platform-sdk/llms.md
- **Repository:** https://github.com/harness/harness-platform-sdk
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

## Testing

This release includes comprehensive test coverage:

```bash
# Run all tests
mise run tests

# Run with coverage report
mise run tests:cov

# Run specific test suite
pytest tests/unit_tests/test_client.py -v
pytest tests/integration_tests/ -v
```

**Coverage Target:** ≥85% (enforced in CI/CD)

---

## Bug Reports & Feature Requests

Please open issues on GitHub:
- **Issues:** https://github.com/harness/harness-platform-sdk/issues
- **Feature Requests:** Tag with `enhancement` label
- **Bug Reports:** Tag with `bug` label

---

## Support

- **Documentation:** https://developer.harness.io/harness-solutions-factory/
- **Issues:** https://github.com/harness/harness-platform-sdk/issues

---

## 🔄 What's Next

**Planned for v1.1.0+:**
- Async API support (native httpx async)
- GraphQL API coverage
- Multi-region orchestration helpers
- Enhanced retry strategies
- Additional domain APIs

---

**License:** BUSL-1.1
**Maintained by:** Harness
**Status:** Production Ready ✅
