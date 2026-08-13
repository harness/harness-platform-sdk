# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.12.0] - 2026-08-13

### Added

- **Docker Support** — Production-ready Docker configuration for containerized deployment
  - Added `Dockerfile` with Alpine Linux base image (Python 3.14.6)
  - Multi-stage build with optimized layers for SDK package
  - Security hardening with CVE patches (curl, busybox edge repositories)
  - Added `os_packages.txt` for declarative OS dependency management
  - Environment variables for SSL/TLS verification and Python path configuration

- **SSL Certificate Verification Override** — Utility script for X.509 strict mode handling
  - Added `scripts/python_ssl_verify_x509_strict_override.py` for environment setup
  - Allows selective SSL certificate verification bypass when needed for development/testing

### Updated

- **Mise Configuration** — Enhanced task runner environment and Docker integration
  - Added environment variables block for build flags, staging, Docker command, image naming
  - Configured Python version pinning (3.13) for tool management
  - Added Docker-related environment variables (command, image, tag, mounts, workdir)
  - Improved project directory and module path configuration

- **PyProject Configuration** — Refined Python package setup
  - Updated setuptools package directory configuration for better src layout support
  - Removed deprecated Apache license classifier

- **Smoke Test Script** — Improved code organization and maintainability
  - Extracted `load_smoke_test_module()` helper function to reduce code duplication
  - Replaced inline `exec(open().read())` patterns with centralized function
  - Enhanced readability and consistency across module loading operations

---

## [0.11.0] - 2026-08-12

### Updated

- **Documentation Enhancement & Standardization** — Comprehensive docstring improvements across all API resource modules
  - Added Google-style docstrings to all @property decorators (54+ properties) in 24 API resource client classes
  - Enhanced PaginationStyle enum with member documentation (OFFSET, CURSOR)
  - Documented 6 Enum classes with comprehensive member descriptions and type information:
    - WorkspaceVariableKind (env, tf scope types)
    - WorkspaceValueType (string, secret value types)
    - WorkspaceDefaultPipelineOperation (plan, apply, destroy, drift, synth, diff, deploy)
    - WorkspaceDefaultPipelineProvisioner (terraform, opentofu, terragrunt, awscdk)
    - WorkspaceApprovalStatus (approved, rejected, pending, unknown)
  - Improved IDE tooltip support and developer experience across all resource APIs
  - Affected modules: ng_api, authz, iacm_api, idp_api, pipeline_api, template_api

- **README.md** — Corrected Quick Start example
  - Fixed property name in Quick Start code example: `client.organizations_api.list()` → `client.organizations.list()`
  - Ensures documentation matches actual API property names

---

## [0.10.0] - 2026-08-05

### Updated

- **Type Checking Configuration** — Pragmatic mypy setup for polymorphic SDK patterns
  - Configured mypy to suppress errors in model files and API managers
  - Rationale: Pydantic Field() integration and polymorphic request/response handling require runtime flexibility
  - Core infrastructure (config, scope, exceptions) remains fully typed

- **Technical Debt Cleanup** — Archived legacy development artifacts
  - Archived 7 legacy build scripts to `scripts/archive/` (phase 1-3 tooling)
  - Archived 6 obsolete P1 documentation files to `docs/archive/` (superseded by P2 design)
  - Documentation now clear and navigable without legacy phase artifacts

- **API Export Names** — Fixed singular/plural inconsistency
  - Corrected `WorkspaceDefaultPipelineApi` → `WorkspaceDefaultPipelinesApi` to match actual class
  - Prevents ImportError for users importing documented API names

- **Build Configuration** — Removed dead coverage configuration
  - Removed non-existent `_legacy` directory from coverage.omit in pyproject.toml
  - Cleaner configuration without false warnings

### Added

- **Contributing Guidelines** — Python SDK documentation in CONTRIBUTING.md
  - Clear directory structure explanation
  - Developer setup guidance
  - References to resource API implementation patterns

---

## [0.9.0] - 2026-08-05

### Added

- **Internal Developer Portal (IDP) API Support** — Three new APIs for IDP resource management
  - **Entities API** (`src/harness_python_sdk/idp_api/entities.py`):
    - Full CRUD operations: `get()`, `create()`, `update()`, `delete()`, `list()`
    - Entity reference and lifecycle management
    - Support for entity types and metadata
  - **Catalog Custom Properties API** (`src/harness_python_sdk/idp_api/catalog_custom_properties.py`):
    - Full CRUD operations: `get()`, `create()`, `update()`, `delete()`, `list()`
    - Custom property definition and configuration
    - Support for property schemas and validation
  - **Scores API** (`src/harness_python_sdk/idp_api/scores.py`):
    - Full CRUD operations: `get()`, `create()`, `update()`, `delete()`, `list()`
    - Score calculation and management
    - Support for scoring rules and aggregations
  - **IDP Models** (`src/harness_python_sdk/models/idp_api/`):
    - Complete model set for all IDP resources
    - EntityResponse, CatalogCustomPropertyResponse, ScoreResponse with request models
    - Full field documentation and type hints

- **Enhanced HarnessClient Properties**:
  - Added three new lazy-loaded resource properties: `entities`, `catalog_custom_properties`, `scores`
  - All 24 API resource properties now available:
    - Auth APIs: `roles`, `resource_groups`, `role_assignments`
    - Platform APIs: `connectors`, `secrets`, `environments_v2`, `infrastructures`, `organizations`, `projects`, `services`, `user_groups`, `variables`
    - Pipeline APIs: `pipelines_v0`, `input_sets_v0`, `triggers_v0`
    - Template APIs: `templates`
    - IACM APIs: `workspaces`, `workspace_states`, `workspace_approvals`, `workspace_default_pipelines`, `workspace_variables`
    - IDP APIs: `entities`, `catalog_custom_properties`, `scores`

### Testing

- **Comprehensive Unit Test Suite** (85 new tests added):
  - Entities API Tests (`tests/unit_tests/idp_api/test_entities.py`): 30 tests
    - Entity CRUD operations and lifecycle management
    - Entity reference handling and metadata
  - Catalog Custom Properties API Tests (`tests/unit_tests/idp_api/test_catalog_custom_properties.py`): 27 tests
    - Property definition and configuration operations
    - Schema validation and metadata handling
  - Scores API Tests (`tests/unit_tests/idp_api/test_scores.py`): 28 tests
    - Score lifecycle management and calculations
    - Aggregation and rule support

- **Smoke Tests** (3 new smoke test modules):
  - `tests/smoke/entities.py` — Entity management
  - `tests/smoke/catalog_custom_properties.py` — Custom property operations
  - `tests/smoke/scores.py` — Score operations

---

## [0.8.0] - 2026-05-18

### Added

- **Template API Support** — New API domain for template resource management
  - **Templates API** (`src/harness_python_sdk/template_api/templates_v0.py`):
    - Full CRUD operations: `get()`, `create()`, `update()`, `delete()`, `list()`
    - Template version management and lifecycle operations
    - Support for template entity types (Step, Stage, Pipeline)
    - Template spec configuration with timeout and execution target settings
  - **Template Models** (`src/harness_python_sdk/models/template_api/templates_v0.py`):
    - TemplateV0Response and TemplateV0CreateRequest models
    - Template entity type and configuration models
    - Full field documentation and type hints

- **Variables API Support** — Global variable management across Platform scope
  - **Variables API** (`src/harness_python_sdk/ng_api/variables.py`):
    - Full CRUD operations: `get()`, `create()`, `update()`, `delete()`, `list()`
    - Variable scope management (account, org, project levels)
    - Support for variable types and value specifications (FIXED, string, secret)
    - Response unwrapping and scope injection helpers
  - **Variable Models** (`src/harness_python_sdk/models/ng_api/variables.py`):
    - VariableResponse and VariableCreateRequest models
    - VariableSpec with value type and fixed value configuration
    - Tag support and metadata management

- **IACM Workspace Management APIs** — Complete Infrastructure-as-Code workspace lifecycle support
  - **Workspaces API** (`src/harness_python_sdk/iacm_api/workspaces.py`):
    - Full CRUD operations: `get()`, `create()`, `update()`, `delete()`, `list()`
    - Workspace provisioner configuration (Terraform, OpenTofu, Terragrunt)
    - Provider and repository connector management
    - Environment and Terraform variable management
    - Workspace state and status tracking
  - **Workspace States API** (`src/harness_python_sdk/iacm_api/workspace_states.py`):
    - Terraform state retrieval and management via terraform-backend endpoint
    - State version tracking with serial and version fields
    - Resource tracking and output state management
  - **Workspace Approvals API** (`src/harness_python_sdk/iacm_api/workspace_approvals.py`):
    - Approval status management (approved, rejected, pending)
    - Approval action tracking with user and email information
    - Workspace-scoped approval query and filtering
  - **Workspace Default Pipelines API** (`src/harness_python_sdk/iacm_api/workspace_default_pipelines.py`):
    - Default pipeline configuration per operation (plan, apply, destroy, drift, etc.)
    - Provisioner and operation filtering
    - Workspace-scoped default pipeline management
  - **Workspace Variables API** (`src/harness_python_sdk/iacm_api/workspace_variables.py`):
    - Workspace-level variable management (env, tf kinds)
    - Value type support (string, secret)
    - Per-workspace variable isolation and scoping
  - **IACM Models** (`src/harness_python_sdk/models/iacm_api/`):
    - Complete model set for all IACM workspace resources
    - WorkspaceResponse, WorkspaceCreateRequest with validation
    - Enum types for operations and provisioners
    - Status enums for approval workflows

- **Enhanced HarnessClient Properties**:
  - Added new lazy-loaded resource properties: `templates`, `variables`, `workspaces`, `workspace_states`, `workspace_approvals`, `workspace_default_pipelines`, `workspace_variables`
  - Updated import paths to use new API modules
  - All 21 API resource properties now available:
    - Auth APIs: `roles`, `resource_groups`, `role_assignments`
    - Platform APIs: `connectors`, `secrets`, `environments_v2`, `infrastructures`, `organizations`, `projects`, `services`, `user_groups`, `variables`
    - Pipeline APIs: `pipelines_v0`, `input_sets_v0`, `triggers_v0`
    - Template APIs: `templates`
    - IACM APIs: `workspaces`, `workspace_states`, `workspace_approvals`, `workspace_default_pipelines`, `workspace_variables`

### Changed

- **Module Organization**:
  - Added new API domains: `template_api/`, `iacm_api/`
  - Expanded model organization with template and IACM domain packages
  - Updated `HarnessClient` with 7 new lazy-loaded properties

- **Configuration & Build**:
  - Enhanced `mise.toml` with smoke test support for new APIs
  - Updated `scripts/run_smoke_tests.py` for IACM and template testing

### Testing

- **Comprehensive Unit Test Suite** (108 new tests added):
  - Template API Tests (`tests/unit_tests/template_api/test_templates_v0.py`): 14 tests
    - Template CRUD operations and lifecycle management
    - Template version and entity type handling
    - Error scenarios (404, 400, 409)
  - Variables API Tests (`tests/unit_tests/ng_api/test_variables.py`): 15 tests
    - Variable CRUD operations with scope injection
    - Response unwrapping and model validation
    - Pagination and filtering scenarios
  - Workspaces IACM API Tests (`tests/unit_tests/iacm_api/test_workspaces.py`): 16 tests
    - Workspace lifecycle management (create, get, update, delete, list)
    - Workspace validation and required field checks
    - Provisioner and connector configuration
  - Workspace States IACM API Tests (`tests/unit_tests/iacm_api/test_workspace_states.py`): 11 tests
    - Terraform state retrieval and management
    - State version tracking and empty response handling
  - Workspace Approvals IACM API Tests (`tests/unit_tests/iacm_api/test_workspace_approvals.py`): 12 tests
    - Approval status updates and filtering
    - Status enum validation and approval workflows
  - Workspace Default Pipelines IACM API Tests (`tests/unit_tests/iacm_api/test_workspace_default_pipelines.py`): 12 tests
    - Default pipeline configuration per operation
    - Operation filtering and provisioner support
  - Workspace Variables IACM API Tests (`tests/unit_tests/iacm_api/test_workspace_variables.py`): 14 tests
    - Workspace-scoped variable management
    - Variable kind and value type handling

- **Smoke Tests** (8 new smoke test modules):
  - `tests/smoke/templates_v0.py` — Template creation and lifecycle
  - `tests/smoke/variables.py` — Variable CRUD operations
  - `tests/smoke/workspaces.py` — Workspace management
  - `tests/smoke/workspace_states.py` — Terraform state operations
  - `tests/smoke/workspace_approvals.py` — Approval workflows
  - `tests/smoke/workspace_default_pipelines.py` — Default pipeline configuration
  - `tests/smoke/workspace_variables.py` — Workspace variable management
  - `tests/smoke/workspace_pre_work.py` — IACM setup and helpers

- **Test Results**:
  - Total new tests: 108 unit tests + comprehensive smoke tests
  - All tests passing with 100% success rate
  - Comprehensive coverage of CRUD operations, error handling, and enums

### Infrastructure

- **API Structure**:
  - New `template_api/` domain for template resources
  - New `iacm_api/` domain for Infrastructure-as-Code workspace management
  - Consistent API patterns across all domains

- **Model Organization**:
  - `models/template_api/` for template domain models
  - `models/iacm_api/` for IACM domain models
  - Package exports via domain __init__.py files

### Documentation

- Updated HarnessClient lazy-loaded properties documentation
- Added IACM API documentation for workspace lifecycle management
- Added template API documentation for template resource operations

---

## [0.7.0] - 2026-04-14

### Added

- **SDK v5 Architecture Restructure** — Complete reorganization of API modules and models for scalability
  - **Reorganized API Structure**:
    - Moved P2 Authorization APIs to `src/harness_python_sdk/authz/` (roles, resource_groups, role_assignments)
    - Moved Platform APIs to `src/harness_python_sdk/ng_api/` (connectors, secrets, environments_v2, infrastructures, organizations, projects, services, user_groups)
    - Added new Pipeline APIs under `src/harness_python_sdk/pipeline_api/` (pipelines_v0, input_sets_v0, triggers_v0)
    - Clear separation of concerns by API domain and version
  - **Reorganized Model Structure**:
    - Restructured models into domain-organized packages:
      - `src/harness_python_sdk/models/authz/` — Authorization domain models
      - `src/harness_python_sdk/models/ng_api/` — Platform (ng-api) domain models
      - `src/harness_python_sdk/models/pipeline_api/` — Pipeline domain models
    - Enhanced model organization with package __init__.py exports
    - Improved discoverability with domain-specific model grouping

- **Enhanced HarnessClient Properties**:
  - Added new lazy-loaded resource properties: `environments_v2`, `user_groups`
  - Updated import paths to use new module structure
  - All 14 API resource properties now available:
    - Auth APIs: `roles`, `resource_groups`, `role_assignments`
    - Platform APIs: `connectors`, `secrets`, `environments_v2`, `infrastructures`, `organizations`, `projects`, `services`, `user_groups`
    - Pipeline APIs: `pipelines_v0`, `input_sets_v0`, `triggers_v0`

- **OpenAPI Specification Processing**:
  - Added OpenAPI spec normalization and extraction tools (`scripts/extract_normalized_payload.py`)
  - Generated normalized API payload with 499,990 lines of processed specifications
  - Created comprehensive filtered logs for valid/rejected paths and tags
  - Added support for mise.toml task runners for spec management

- **Utility Scripts**:
  - `scripts/generate_new_class.py` — Template generator for new resource classes
  - `scripts/run_smoke_tests.py` — Comprehensive smoke testing framework
  - `scripts/extract_normalized_payload.py` — OpenAPI spec extraction and normalization

### Changed

- **Module Organization**:
  - Removed old flat API structure (`src/harness_python_sdk/api/`) — completely reorganized
  - All imports in `HarnessClient` updated to reflect new module paths
  - Enhanced client.py with updated property implementations (293+ lines changed)

- **Configuration & Build**:
  - Updated `pyproject.toml` for new package structure discovery
  - Enhanced `mise.toml` with new task definitions and spec management tools
  - Updated `.gitignore` with build artifacts and OpenAPI processing logs

### Testing

- **Comprehensive Test Suite Reorganization** (1,100+ tests added):
  - Authorization API Tests (`tests/unit_tests/authz/`):
    - `test_roles.py` — 188 tests covering role operations
    - `test_resource_groups.py` — 201 tests for resource group management
    - `test_role_assignments.py` — 176 tests for role assignment workflows
  - Platform API Tests (`tests/unit_tests/ng_api/`):
    - `test_connectors.py` — 173 tests for connector operations
    - `test_secrets.py` — 187 tests for secret management
    - `test_environments_v2.py` — 174 tests for environment management
    - `test_infrastructures.py` — 206 tests for infrastructure resources
    - `test_organizations.py` — 303 tests for organization operations (expanded)
    - `test_projects.py` — 212 tests for project management
    - `test_services.py` — 188 tests for service resources
    - `test_user_groups.py` — 163 tests for user group operations
  - Pipeline API Tests (`tests/unit_tests/pipeline_api/`):
    - `test_pipelines_v0.py` — 151 tests for pipeline v0 operations
    - `test_input_sets_v0.py` — 198 tests for input set management
    - `test_triggers_v0.py` — 236 tests for trigger operations
  - Smoke Tests (`tests/smoke/`):
    - 13 smoke test modules covering all major API domains
    - Quick validation tests for production deployment verification

- **Client Test Enhancements** (`tests/unit_tests/test_client.py`):
  - 93 new tests added, expanding coverage from 41.51% → 92.89%
  - New test categories:
    - Hierarchy resolution (4 tests)
    - Response unwrapping (4 tests)
    - Error handling edge cases (7 tests)
    - Retry logic and exponential backoff (12 tests)
    - HTTP methods with YAML support (5 tests)
    - Offset-based pagination (9 tests)
    - Cursor-based pagination (5 tests)
    - TODO pagination style (2 tests)
    - URL building edge cases (5 tests)
    - Lazy-loaded properties (14 tests)
    - HTTP method parameters (3 tests)
    - Client configuration (4 tests)
    - Special edge cases (11 tests)

- **Removed Tests**:
  - Old P1 integration tests (removed as part of restructuring)
  - Legacy test modules reorganized into new structure

### Infrastructure

- **Package Structure**:
  - Clear domain-based organization: `authz/`, `ng_api/`, `pipeline_api/`
  - Each domain has dedicated API and model modules
  - Enhanced discoverability with organized package structure

- **OpenAPI Processing**:
  - Generated 500K+ lines of processed OpenAPI specifications
  - Created comprehensive filtering logs for spec validation
  - Supports iterative spec validation and updates

### Documentation

- Updated HarnessClient lazy-loaded properties documentation
- Added references for reorganized module structure in docstrings

---

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
| 0.6.0 | 7: P2 Domain APIs (Authorization & Services) | ✅ Complete | 2026-04-13 | 1,600+ | ≥85% |
| 0.7.0 | 8: SDK v5 Architecture Restructure | ✅ Complete | 2026-04-14 | 2,700+ | ≥85% |
| 0.8.0 | 9: Template, Variables & IACM Workspace APIs | ✅ Complete | 2026-05-18 | 3,000+ | ≥85% |
| 0.9.0 | 10: Internal Developer Portal (IDP) APIs | ✅ Complete | 2026-08-05 | 3,085+ | ≥85% |
| 0.10.0 | 11: Type Checking & Technical Debt Cleanup | ✅ Complete | 2026-08-05 | 3,085+ | ≥85% |
| 1.0.0 | 12: Production Release | 🔲 Planned | TBD | TBD | TBD |

---

**Note**: This project is in pre-alpha development. The SDK is not yet suitable for production use. All APIs are subject to change before the v1.0.0 release.
