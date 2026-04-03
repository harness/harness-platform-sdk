# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-03

### Added

- **Branch 2: Core Client** — Foundation for all domain APIs
- **HarnessClient** — Main SDK entry point with:
  - HTTP methods (GET, POST, PUT, PATCH, DELETE) with automatic retry
  - Status-code retry logic (429, 503) with Retry-After header support
  - Scope resolution (merges call-time and default scopes)
  - URL template substitution for {account_id}, {org}, {project}
  - Pagination support for both OFFSET (pageIndex/pageSize) and CURSOR (nextPageToken) styles
  - Context manager and explicit close() for resource cleanup
- **Configuration** — HarnessConfig with all necessary settings
  - API key, account ID, base URL, timeout, retry settings
  - Configurable retry behavior (status codes, max attempts, enable/disable)
  - SSL verification control
- **Exception Hierarchy** — Comprehensive error handling
  - HarnessSdkError (base), ScopeNotSetError, ApiError, AuthError
  - All exceptions preserve status code, response body, and headers (API key redacted)
- **Scope Management** — Frozen Pydantic model for request context
  - Account ID (required), org and project (optional)
  - Immutable after creation for safety
- **Base Models** — Pydantic v2 foundation
  - HarnessModel with extra fields allowed and alias support
- **Pagination** — PaginationStyle enum and client implementation
  - Offset-based pagination (pageIndex/pageSize with pageItemCount detection)
  - Cursor-based pagination (nextPageToken loop)
  - Both styles yield individual items as they're fetched

### Testing

- 110 comprehensive tests covering:
  - Config, exceptions, scope (41 tests)
  - Pagination enum (9 tests)
  - Client construction and lifecycle (10 tests)
  - Scope resolution decision tree (6 tests)
  - Retry behavior (429, 503, Retry-After, max_retries, config override) (7 tests)
  - HTTP methods (9 tests)
  - Pagination (both OFFSET and CURSOR styles) (7 tests)
  - Additional regressions and edge cases
- **Coverage:** 89.43% (target: 85%) ✅

### Infrastructure

- **pyproject.toml** — Build configuration with Pydantic v2, httpx, tenacity
- **mise.toml** — Task runner with placeholder tasks for Branch 3
- **Python 3.11+** — Modern language features (union syntax, walrus operator)
- **Pydantic v2** — No v1 shims, modern validation patterns

---

## [0.0.1] - 2026-04-02

### Added

- Initial repository setup with project scaffolding (Python 3.11+, Pydantic v2, httpx)
- Project configuration and tooling:
  - `.gitignore` and `.editorconfig` configuration
  - `CONTRIBUTING.md` guidelines
  - MIT License
  - `.claude/settings.json` for development environment
- **Harness OpenAPI Specification** (12 MB, 1,884 endpoints):
  - Complete OpenAPI v3.0 specification from Harness platform
  - Covers 13 domains: pipelines, connectors, secrets, infrastructure, access_control, environments, projects, organizations, cost, governance, cloud, audit, other
  - Stored at `openapi/harness-openapi.yaml`
- **Branch 1: Spec Analysis Spike** - Proof of concept validation:
  - Model generation spike with datamodel-code-generator
  - Pagination inventory analysis for all 1,884 endpoints
  - Spec quality issue identification and documentation
- **Technical Documentation**:
  - `docs/spike-model-count.md` - Model generation analysis (88 models generated, ✅ PASS verdict)
  - `docs/pagination_inventory.md` - Complete pagination patterns inventory (940 list endpoints analyzed)

---

## Version History

| Version | Branch | Status | Release Date |
|---------|--------|--------|--------------|
| 0.0.1 | 1: Spec Analysis Spike | ✅ Complete | 2026-04-02 |
| 0.1.0 | 2: Core Client | ✅ Complete | 2026-04-03 |
| 0.2.0 | 3: Model Generation Pipeline | 🔲 Planned | TBD |
| 0.3.0 | 4: Domain APIs | 🔲 Planned | TBD |
| 1.0.0 | 5: Test Suite Hardening | 🔲 Planned | TBD |

---

**Note**: This project is in pre-alpha development. The SDK is not yet suitable for production use. All APIs are subject to change before the v1.0.0 release.
