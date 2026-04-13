# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2026-04-13

### Added

- **P2 Domain APIs** — Six production-ready API domains for Account-level Access Control and IAM
  - **Organizations API** (`src/harness_python_sdk/api/organizations.py`):
    - Full CRUD operations: `list()`, `get()`, `create()`, `update()`, `delete()`
    - Automatic pagination support with response envelope unwrapping
    - Request/Response models with organization metadata (createdAt, lastModifiedAt, harnessManaged)
  - **Projects API** (`src/harness_python_sdk/api/projects.py`):
    - Complete project lifecycle management across organizations
    - List, create, update, and delete operations with full type safety
  - **Roles API** (`src/harness_python_sdk/api/roles.py`):
    - Role definition and management
    - Support for built-in and custom roles
    - Role query and assignment capabilities
  - **Role Assignments API** (`src/harness_python_sdk/api/role_assignments.py`):
    - User/service account role assignment operations
    - Scope-aware assignment (account, org, project level)
    - Bulk assignment and removal support
  - **Resource Groups API** (`src/harness_python_sdk/api/resource_groups.py`):
    - Resource group creation and management
    - Support for scoped resource filtering
    - Integration with RBAC workflows
  - **Services API** (`src/harness_python_sdk/api/services.py`):
    - Service resource management (distinct from Harness Services product)
    - List, create, update, delete operations
  - **P2 Domain Models** (`src/harness_python_sdk/models/`):
    - Hand-authored Pydantic models for all six P2 domains
    - Response and Create/Update request models for each resource
    - Full field documentation and type hints
  - **Lazy-loaded API Properties** on `HarnessClient`:
    - `client.organizations`, `client.projects`, `client.roles`, `client.role_assignments`, `client.resource_groups`, `client.services`
    - Seamless integration with existing P1 APIs (pipelines, connectors, secrets, infrastructure)

### Changed

- **HarnessClient API Properties**:
  - Added six new lazy-loaded P2 API properties
  - Maintains backward compatibility with existing P1 API properties
  - All properties initialize on first access to avoid overhead

### Testing

- **P2 Domain Integration Tests** (1,323 new tests):
  - Branch 2 (B1) Integration: Organizations, Projects lifecycle (497 tests)
  - Branch 3 (B2) Integration: Roles, Resource Groups, Role Assignments (292 tests)
  - Branch 4 (B3) Integration: Services and advanced RBAC scenarios (534 tests)
  - Full request/response flow validation
  - Pagination testing across all P2 domains
  - Error mapping and exception handling
  - Multi-scope operations (account, org, project level)

### Documentation

- **P1 Endpoint Inventory** (`docs/p1_endpoint_inventory.md`):
  - Complete P1 domain endpoint reference (Pipelines, Connectors, Secrets, Infrastructure)
  - Endpoint patterns, request/response structures, pagination details
  - Quick lookup guide for all P1 operations

- **P2 Envelope Audit** (`docs/p2_envelope_audit.md`):
  - Analysis of all P2 domain API response envelopes
  - Response structure patterns across six P2 domains
  - Envelope unwrapping strategies for each domain

- **P2 Model Fields** (`docs/p2_model_fields.md`):
  - Comprehensive field specifications for all six P2 domains
  - Request/Response field mappings with required/optional indicators
  - Type information and validation constraints for each field

- **Pagination Inventory Update** (`docs/pagination_inventory.md`):
  - Updated pagination patterns including all P2 domains
  - Classification of all list endpoints as OFFSET, CURSOR, or UNKNOWN
---

## [0.5.0] - 2026-04-09

### Added

- **P1 Integration Test Suite** — Comprehensive integration tests for all P1 domains
  - **P1 Integration Test Reference** (`docs/p1_integration_test_reference.md`):
    - Complete reference guide for P1 API endpoints (Pipelines, Connectors, Secrets, Infrastructure)
    - Minimal mock payload examples for all four domains
    - Pagination pattern documentation for OFFSET-based pagination
    - URL patterns with scope substitution (test-org/test-project)
  - **Full Integration Tests** (`tests/integration/test_p1_integration.py`):
    - 636 lines of comprehensive integration test coverage
    - Six required test scenarios across all P1 domains:
      1. 2-page auto-pagination with OFFSET style
      2. Typed get() with URL and model confirmation
      3. create() with x-api-key header and request body verification
      4. ScopeNotSetError when scope not set
      5. 429 retry via tenacity
      6. 401 AuthError with ApiError inheritance
    - Uses pytest-httpx mocking for full request/response flow validation
    - Validates request bodies and response models for all four domains

### Changed

- **HarnessClient HTTP Header Enhancement**:
  - Added `x-account-id` header to all HTTP requests
  - Required for proper request routing on account-scoped operations
  - Complements existing `x-api-key` and `Content-Type` headers

- **P1 API Method Signatures** — Cleanup of unused parameters:
  - Removed `body=None` parameter from `_get()` calls in all P1 API methods
  - Removed `body=None` parameter from `_delete()` calls in all P1 API methods
  - Affects: Pipelines, Connectors, Secrets, Infrastructure APIs
  - Simplifies method signatures without changing functionality

### Testing

- **Integration Tests** — New comprehensive P1 test suite:
  - Full request/response flow validation for Pipelines, Connectors, Secrets, Infrastructure
  - pytest-httpx mocking for deterministic test execution
  - Header validation (x-api-key, x-account-id, Content-Type)
  - Request body verification for create operations
  - Response model type confirmation
  - Pagination end-of-results detection
  - Retry behavior (429 with tenacity)
  - Error mapping (401 AuthError)
  - Scope validation (ScopeNotSetError)

### Documentation

- **P1 Integration Reference** — New reference guide for developers:
  - Quick lookup for all P1 endpoint patterns
  - Mock payload examples for testing
  - Pagination style documentation
  - Scope substitution patterns

## [0.4.0] - 2026-04-08

### Added

- **Branch 4.5: P1 Domain APIs** — Four production-ready API domains for Pipelines, Connectors, Secrets, and Infrastructure
  - **Pipelines API** (`src/harness_python_sdk/api/pipelines.py`):
    - Full CRUD operations: `list()`, `get()`, `create()`, `update()`, `delete()`
    - Automatic pagination support via offset-based pagination
    - Request/Response models with camelCase ↔ snake_case mapping
  - **Connectors API** (`src/harness_python_sdk/api/connectors.py`):
    - Full CRUD operations with support for diverse connector types
    - Polymorphic `spec` field for connector-specific configuration
    - Account-scoped and organization-scoped operations
  - **Secrets API** (`src/harness_python_sdk/api/secrets.py`):
    - Secret management across account, organization, and project scopes
    - Support for different secret types (SecretText, SecretFile, SecretRef)
    - Draft state support for secret management workflows
  - **Infrastructure API** (`src/harness_python_sdk/api/infrastructure.py`):
    - Infrastructure definition and management
    - Support for multiple infrastructure types (Kubernetes, SSH, WinRm, etc.)
    - Environment-scoped operations for multi-environment deployments
  - **P1 Domain Models** (`src/harness_python_sdk/models/`):
    - Hand-authored Pydantic models for all four P1 domains
    - Response models for reading resources
    - Create/Update request models for mutation operations
    - All models inherit from `HarnessModel` with `extra="allow"` and `populate_by_name=True`
  - **Lazy-loaded API Properties** on `HarnessClient`:
    - `client.pipelines`, `client.connectors`, `client.secrets`, `client.infrastructure`
    - Avoid circular imports and reduce initialization overhead
  - **Enhanced Pagination** (`src/harness_python_sdk/client.py`):
    - Added `unwrap_field` parameter to `_paginate()` for nested response structures
    - Support for both direct array responses (v1 endpoints) and nested `data.content` (ng-api endpoints)
    - Automatic pagination metadata extraction for accurate page termination
  - **P1 API Documentation** (`docs/p1_model_fields.md`):
    - Complete field specifications for all four P1 domains
    - Endpoint paths, pagination styles, and field type information
    - Request/Response field mappings with camelCase aliases

### Fixed

- **Pagination Response Structure Handling**:
  - Fixed bug where Connectors and Secrets list operations failed with `TypeError: argument after ** must be a mapping, not str`
  - Root cause: API responses use different structures (direct array vs. nested `data.content`) and wrap items in domain-specific fields
  - Solution: Enhanced `_paginate()` to detect and extract both response patterns, added `unwrap_field` parameter to API methods
  - Affects: All ng-api list endpoints (Connectors, Secrets, Infrastructure) now correctly parse paginated responses

### Changed

- **HarnessClient HTTP Method Signatures**:
  - Enhanced `_get()`, `_post()`, `_put()`, `_delete()` to support both `body` and `response_model` parameters for consistency
  - Maintains backward compatibility with existing code

### Testing

- **P1 Domain Tests** (68 new tests):
  - 32 unit tests for P1 models: field validation, aliases, inheritance
  - 29 integration tests: API presence, method signatures, scope validation, typed request handling
  - 7 pagination tests: offset pagination, cursor pagination, direct arrays, nested structures
  - All tests pass with 100% coverage of public APIs
- **No Regressions**:
  - Existing client_core tests continue to pass (169 tests)
  - Drift detection tooling unchanged
  - Pagination behavior preserved for all existing endpoints

## [0.3.0] - 2026-04-08

### Added

- **Branch 4: Drift Detection & Model Cleanup** — Production-ready spec monitoring and cleanup
  - **Permanent Drift Detection Tooling** (`scripts/check_drift.py`):
    - Graduated from spike implementation with full x-tagGroups coverage
    - Dynamic domain resolution from all 34 Harness API domains (no hardcoding)
    - Endpoint-granularity checksums: 1,071 endpoints indexed per-operation
    - Baseline stored in `docs/model_checksums.json` with ISO date tracking
    - `--compare` mode: exits non-zero on CHANGED or REMOVED endpoints, non-blocking on ADDED
    - Canonical schema extraction (strips descriptions, examples, x-* extensions)
    - One-level ref resolution with comprehensive error handling
  - **Pagination Inventory Regeneration** (`scripts/refresh_pagination.py`):
    - Standalone tool for keeping pagination patterns current
    - Classifies 333+ list endpoints as OFFSET, CURSOR, or UNKNOWN
    - Fully idempotent: running multiple times produces identical output
    - Markdown table output grouped by domain with evidence trails
    - Integrates with same x-tagGroups domain resolution as drift detection
  - **Specification Repairs Audit Trail** (`docs/spec_repairs.json`):
    - Now fully idempotent with sorted entries by schema name
    - Uses relative paths (e.g., `openapi/harness-openapi.yaml`) for portability
    - Consistent output across runs and commits
    - Enables reliable spec evolution tracking
  - **Model Cleanup** — Removed incomplete auto-generated models:
    - Chaos domain models (37 files removed) — waiting for stabilization
    - Governance domain models (3 files removed) — incomplete mappings
    - Infrastructure models (1 file removed) — deprecated v2 approach
    - Pipelines domain models (3 files removed) — superseded by direct API usage
    - Misc domain cleanup (120+ files removed) — consolidated internal models
    - Reduced model count from 1,200+ to focused set of stable, essential models
    - Verified no public API impact (hand-authored models remain unchanged)

### Changed

- **mise.toml** — Wired drift tooling, streamlined generation pipeline
  - New tasks: `check-drift` (compare mode), `baseline` (generate checksums), `refresh-pagination`
  - Renamed spec tasks: `spec:fetch` → `fetch-spec`, `spec:normalize` → `normalize-spec`, etc.
  - Retired old generation pipeline: `convert-spec`, `generate-models`, `sort-models` now no-ops
  - Updated `regenerate` chain: `fetch-spec && normalize-spec` only (generation pipeline retired)
  - Task names normalized to hyphenated format for consistency
- **OpenAPI Normalized Spec** — Full regeneration with current repairs:
  - 368K line normalized YAML with all 1,587 repairs applied
  - 5,300 lines modified for consistency and correctness
  - Inline response promotion, discriminator fixes, schema normalization
- **normalize_spec.py** — Enhanced idempotency:
  - Sorts all repair entries by schema name before output
  - Converts paths from absolute to relative for version control portability

### Removed

- **Auto-Generated Models** — Cleaned up incomplete or experimental domains:
  - 119 files removed (14,046 lines)
  - Chaos, governance, infrastructure (v2), pipelines, and misc subdomain models
  - Reason: These domains lack stable APIs or require manual review before SDK integration
  - Future: Can be re-generated when APIs stabilize using `mise run regenerate`
  - Keeps codebase lean and focused on hand-authored, tested resources

### Infrastructure

- **Drift Detection Pipeline**:
  - Compares current spec checksums against baseline for early drift alerting
  - Supports `mise run check-drift` for CI/CD integration (exits non-zero on breaking changes)
  - Regenerates baseline with `mise run baseline` when spec intentionally updates
- **Idempotent Specification Artifacts**:
  - `docs/model_checksums.json` — Per-endpoint checksums and per-domain aggregates
  - `docs/pagination_inventory.md` — Auto-regenerated list endpoint analysis
  - `docs/spec_repairs.json` — Sorted, relative-path audit trail
  - All three files are fully deterministic (timestamp-only variance expected)

### Testing

- Updated smoke tests to reflect cleaned-up model set:
  - Removed test cases for deleted chaos, governance, infrastructure, pipelines domains
  - Maintained coverage for stable, supported domains
  - All tests passing with cleaned-up imports

### Documentation

- Created completion report with full implementation details
- Documented known gaps in drift detection (requestBodies, recursive refs)
- Provided rationale for model cleanup (consolidation and API evolution)

---

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
| 0.3.0 | 4: Drift Detection & Cleanup | ✅ Complete | 2026-04-08 | TBD | TBD |
| 0.4.0 | 5: Domain APIs (P1 Production APIs) | ✅ Complete | 2026-04-08 | TBD | TBD |
| 0.5.0 | 6: P1 Integration Test Suite | ✅ Complete | 2026-04-09 | TBD | TBD |
| 1.0.0 | 7: Test Suite Hardening | 🔲 Planned | TBD | TBD | TBD |

---

**Note**: This project is in pre-alpha development. The SDK is not yet suitable for production use. All APIs are subject to change before the v1.0.0 release.
