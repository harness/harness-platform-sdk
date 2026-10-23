# Terraform Fixtures for Harness Platform SDK Smoke Tests

This directory contains OpenTofu/Terraform configurations that provision test infrastructure for the Harness Platform SDK smoke tests.

## Overview

Smoke tests require a pre-provisioned Harness environment with foundational resources (organization, project, pipelines, secrets, connectors, etc.). These fixtures define all required resources using Infrastructure-as-Code (IaC), enabling reproducible test environments across different development and CI/CD contexts.

**Provider:** Harness Terraform Provider (`harness/harness`)  
**Compatibility:** OpenTofu 1.10+ (recommended) or Terraform 1.10+

## File Structure

| File | Purpose |
|------|---------|
| `terraform.tf` | Terraform version and provider constraints |
| `providers.tf` | Harness provider configuration and authentication variables |
| `variables.tf` | Input variables (e.g., feature flags) |
| `locals.tf` | Local values and shared configuration (tags, formats) |
| `main.tf` | Resource definitions (orgs, projects, pipelines, connectors, IDP entities) |
| `timers.tf` | Tier-based sleep resources to enforce creation ordering |
| `.terraform/` | OpenTofu/Terraform plugin cache (auto-generated) |

## Prerequisites

1. **OpenTofu or Terraform CLI**
   ```bash
   # Install OpenTofu (recommended)
   brew install opentofu

   # Or use Terraform
   brew install terraform
   ```

2. **Harness Account Credentials**
   - Account ID
   - Platform API key
   - (Optional) Custom Harness endpoint URL

3. **Environment Variables**
   ```bash
   export HARNESS_ACCOUNT_ID="your-account-id"
   export HARNESS_PLATFORM_API_KEY="your-api-key"
   export HARNESS_ENDPOINT="https://app.harness.io"  # Optional
   ```

## Quick Start

### Initialize and Provision

```bash
# Navigate to the fixtures directory
cd tests/fixtures/terraform

# Initialize OpenTofu/Terraform (download provider plugins)
tofu init
# or: terraform init

# Preview resources to be created
tofu plan
# or: terraform plan

# Apply configuration and provision resources
tofu apply
# or: terraform apply
```

### Destroy Fixtures

```bash
# Remove all provisioned resources
tofu destroy
# or: terraform destroy
```

## Resource Hierarchy

Resources are organized into **tiers** to enforce dependency ordering and allow API propagation between creations. Each tier includes a sleep timer (see `timers.tf`):

### Foundation (Tier 0)
- **Organization:** `PLATFORM_SDK_FIXTURES`
- **Project:** `FIXTURE_PLACEHOLDER`

These are the root containers for all other resources.

### Tier 1 (5s delay after foundation)
Foundational project-scoped resources:
- **Pipeline:** `default_list_pipeline` — minimal shell script pipeline
- **Environment:** `default_list_environment` — PreProduction environment
- **Secret:** `default_list_secret` — text secret for connector credentials
- **Pipeline:** `default_iacm_pipeline` — OpenTofu orchestration pipeline (init, plan, apply, destroy)

### Tier 2 (5s delay after Tier 1)
Secondary resources depending on Tier 1:
- **Connector:** `default_list_connector` — GitHub connector (uses `default_list_secret`)

### Tier 3 (5s delay after Tier 2)
Advanced resources depending on lower tiers:
- **Workspace:** `default_list_workspace` — IACM workspace (uses GitHub connector and IACM pipeline)
- **IDP Catalog Entity:** `default_idp_catalog_entity` — component service for catalog
- **IDP Scorecard Check:** `default_idp_scorecard_check` — quality check (README.md exists)
- **IDP Scorecard:** `default_idp_scorecard` — quality scorecard with baseline metrics

## Resource Identifiers

All resource identifiers are hardcoded to match references in `scripts/run_smoke_tests.py`. **Do not change these identifiers** unless you also update the smoke test runner script.

| Resource | Identifier | Used In Test(s) |
|----------|-----------|-----------------|
| Organization | `PLATFORM_SDK_FIXTURES` | All tiers |
| Project | `FIXTURE_PLACEHOLDER` | All tiers |
| Pipeline | `default_list_pipeline` | `pipelines_v0.py`, `triggers_v0.py` |
| Environment | `default_list_environment` | `environments_v2.py` |
| Secret | `default_list_secret` | `secrets.py` |
| Connector | `default_list_connector` | `connectors.py`, workspace provisioning |
| Pipeline (IACM) | `default_iacm_pipeline` | `workspace_default_pipelines.py` |
| Workspace | `default_list_workspace` | `workspaces.py`, `workspace_states.py`, `workspace_variables.py` |
| IDP Entity | `default_idp_catalog_entity` | `entities.py` |
| Scorecard Check | `default_idp_scorecard_check` | `scores.py` |
| Scorecard | `default_idp_scorecard` | `scores.py` |

## Authentication

The Harness provider reads credentials from environment variables in this order:

1. **Variable values** (if passed via `-var` or terraform.tfvars)
2. **Environment variables:**
   - `HARNESS_ENDPOINT` → provider `endpoint`
   - `HARNESS_ACCOUNT_ID` → provider `account_id`
   - `HARNESS_PLATFORM_API_KEY` → provider `platform_api_key`

### Example: Load from .env file

Create a `.env` file with your credentials:

```bash
export HARNESS_ACCOUNT_ID="abc123"
export HARNESS_PLATFORM_API_KEY="xyzkey"
export HARNESS_ENDPOINT="https://app.harness.io"
```

Then apply it before running tofu/terraform:

```bash
source .env
tofu apply
```

## Tagging Strategy

All resources are tagged with:
- `created_by: Terraform` — Origin tracking
- `plugin_test: true` — Test environment marker
- `plugin: harness-platform-sdk` — Project identifier

These tags help identify test resources in your Harness account and facilitate cleanup.

## Customization

### Adding Resources

1. Edit `main.tf` to define new resources
2. Use appropriate tier (`depends_on` constraint) based on resource dependencies
3. Add identifiers to `scripts/run_smoke_tests.py` fixture scope if tests need to reference them
4. Update smoke test files to use the new resource identifiers

### Feature Flags

The `should_run_second` variable (in `variables.tf`) can enable additional fixture resources:

```bash
tofu apply -var="should_run_second=true"
```

Edit `second.tf` to define optional resources (if it exists; currently not included).

## Troubleshooting

### Provider Installation Fails

```bash
# Force provider redownload
rm -rf .terraform/providers
tofu init
```

### Resources Already Exist

If resources with these identifiers already exist in your account:

```bash
# Adopt existing resources into state
tofu import harness_platform_organization.core PLATFORM_SDK_FIXTURES

# Or use a different project/org identifier
tofu apply -var="org_identifier=SDK_FIXTURES_ALT"
```

### Tier Timeouts (Resource Still Pending)

The tier delays (5-10s) assume normal API latency. If experiencing slow API responses:

```bash
# Edit timers.tf to increase delays, or
tofu apply -var="tier_delay=15"  # if variables exist for this
```

## Integration with Smoke Tests

After provisioning, run smoke tests:

```bash
cd ../../..
python scripts/run_smoke_tests.py
```

The test runner injects fixture resource identifiers into each test module's global namespace, allowing tests to reference:
- `client` — authenticated HarnessClient
- `global_org_id`, `global_project_id`
- `global_project_pipeline_id`, `global_project_connector`, etc.

## References

- [Harness Terraform Provider Documentation](https://registry.terraform.io/providers/harness/harness)
- [OpenTofu Documentation](https://opentofu.org/)
- [Harness Platform SDK Smoke Tests](../../scripts/run_smoke_tests.py)
