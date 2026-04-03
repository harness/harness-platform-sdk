# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-03

### Added

- **Branch 3: Model Generation Pipeline** — Automated OpenAPI model generation with quality control
  - **Spec Normalization Engine** (`scripts/normalize_spec.py`):
    - Fixes 4 categories of Harness OpenAPI spec defects (763 total repairs)
    - Malformed `required` fields (3 fixed): Property-level → schema-level promotion
    - Broken discriminator mappings (36 fixed): Removes invalid schema references
    - Empty schemas (487 fixed): Adds well-formed `properties: {}`
    - Inline response promotion (237 fixed): Generates refs for inline schemas
    - Generates `docs/spec_repairs.json` audit trail for full traceability
  - **YAML→JSON Conversion** (`scripts/convert_spec.py`):
    - Converts normalized OpenAPI YAML to JSON for code generation
    - Validates output (16.4 MB JSON spec)
  - **Model Post-Processing** (`scripts/stamp_generated.py`):
    - Adds `# GENERATED — do not edit...` header to all generated files
    - Rewrites `BaseModel` → `HarnessModel` inheritance
    - Ensures Pydantic v2 config (extra="allow", populate_by_name=True)
  - **Domain Model Organization** (`scripts/sort_models.py`):
    - Distributes 89 generated models across 14 domains + misc
    - Domains: pipelines, connectors, secrets, infrastructure, access_control, environments, projects, organizations, cost, governance, cloud, audit, gitops, chaos
    - Fully idempotent sorting algorithm
    - Creates domain directories with package markers
  - **Comprehensive Smoke Test** (`tests/unit_tests/test_models_smoke.py`):
    - 18 test cases validating all 14 domains + misc
    - Verifies HarnessModel inheritance and Pydantic config
    - Tests extra field allowance and camelCase population
    - Confirms all domain packages are importable

### Changed

- **mise.toml** — Added complete model generation pipeline:
  - `normalize-spec`: Spec quality fixes
  - `convert-spec`: YAML→JSON conversion
  - `generate-models`: datamodel-code-generator with post-processing
  - `sort-models`: Domain sorting and organization
  - `regenerate`: Full end-to-end chain (normalize → convert → generate → sort)
- **pyproject.toml** — Updated package discovery to include models namespace
- **Infrastructure improvements**:
  - `openapi/harness-openapi-normalized.yaml` (368K lines) — Normalized spec artifact
  - `openapi/harness-openapi-normalized.json` — JSON version for code generation
  - `scripts/inline_response_map.json` — Inline schema promotion audit
  - 15 domain directories with `.gitkeep` for tracking

### Infrastructure

- **Code Generation Pipeline** — Fully automated from raw spec to domain-organized models
  - Uses datamodel-code-generator 0.55.0 with Pydantic v2 backend
  - Gracefully handles generator limitations (omits --collapse-root-models and --use-alias-generators)
  - Post-processing ensures all models stamped and properly inherited
  - All generated artifacts are version-controlled for reproducibility
- **Package Structure** — Models organized into semantic domains
  - Enables future branch 4 implementation (domain-specific API files)
  - Provides clear separation of concerns across 14 Harness domains

### Testing

- Added 18 new test cases covering:
  - Model generation and inheritance (all 14 domains)
  - HarnessModel config (extra fields, alias support)
  - Package discovery and __init__.py presence
  - GENERATED header verification
- **Total test count:** 134 tests (117 existing + 17 new)
- **Coverage:** Maintained ≥85% on src/harness_python_sdk (models excluded per spec)
- **Regressions:** 0 ✅

### Fixes

- **v3 Improvement:** Fixed __init__.py handling in post-processing
  - datamodel-code-generator creates complex __init__ files with imports
  - Post-processing now ensures all __init__.py files are simple markers
  - Prevents import chain failures and ensures clean domain imports
  - Verified with full regeneration cycle: all 134 tests passing

---

## [0.1.1] - 2026-04-03

### Added

- **Configurable Base URL** — HarnessClient now supports custom Harness instances
  - `base_url` kwarg in `HarnessClient.__init__()` for convenient construction
  - `base_url` property (getter/setter) for runtime updates
  - Setter atomically closes old session and opens new one with updated URL
  - Default remains `https://app.harness.io` for backward compatibility
  - Supports both kwarg and explicit config construction patterns

### Changed

- **Internal refactoring:** Extracted `_build_http_client()` helper to support base URL updates
- No breaking changes to existing public API

### Testing

- Added 7 new test cases covering:
  - Construction with `base_url` kwarg (with/without defaults)
  - Explicit config with `base_url`
  - Base URL property getter and setter behavior
  - Session lifecycle on URL changes (no leaks)
  - Multi-reassignment scenarios
- **Coverage:** 89.67% (maintained above 85% target) ✅

---

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

| Version | Feature | Status | Release Date | Tests | Coverage |
|---------|---------|--------|--------------|-------|----------|
| 0.0.1 | 1: Spec Analysis Spike | ✅ Complete | 2026-04-02 | N/A | N/A |
| 0.1.0 | 2: Core Client | ✅ Complete | 2026-04-03 | 110 | 89.43% |
| 0.1.1 | 2.1: Configurable Base URL | ✅ Complete | 2026-04-03 | 117 | 89.67% |
| 0.2.0 | 3: Model Generation Pipeline | ✅ Complete | 2026-04-03 | 134 | ≥85% |
| 0.3.0 | 4: Domain APIs | 🔲 Planned | TBD | TBD | TBD |
| 1.0.0 | 5: Test Suite Hardening | 🔲 Planned | TBD | TBD | TBD |

---

**Note**: This project is in pre-alpha development. The SDK is not yet suitable for production use. All APIs are subject to change before the v1.0.0 release.
