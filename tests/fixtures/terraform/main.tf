# Query current Harness account context (used for validation/reference)
data "harness_platform_current_account" "this" {}

# ============================================================================
# FOUNDATION TIER: Organization and Project
# These resources are the base for all subsequent resources
# ============================================================================

# Root organization for SDK test fixtures
# Identifier must match: PLATFORM_SDK_FIXTURES (referenced in run_smoke_tests.py)
resource "harness_platform_organization" "core" {
  identifier  = "PLATFORM_SDK_FIXTURES"
  name        = "PLATFORM_SDK_FIXTURES"
  description = "Automated Project Creation for Testing harness-platform-sdk"
  tags        = ["created_by:Terraform", "plugin_test:true", "plugin:harness-platform-sdk"]
}

# Root project for SDK test fixtures
# Identifier must match: FIXTURE_PLACEHOLDER (referenced in run_smoke_tests.py)
resource "harness_platform_project" "core" {
  identifier  = "FIXTURE_PLACEHOLDER"
  name        = "FIXTURE_PLACEHOLDER"
  description = "Automated Project Creation for Testing harness-platform-sdk"
  org_id      = harness_platform_organization.core.id
  tags        = ["created_by:Terraform", "plugin_test:true", "plugin:harness-platform-sdk"]
}

# ============================================================================
# TIER 1: Foundational project resources
# Pipelines, environments, secrets, and connectors that other resources depend on
# Waits for foundation tier to complete via harness_time_sleep.tier_1
# ============================================================================

# Default pipeline for smoke tests (pipelines_v0.py and triggers_v0.py)
# Identifier must match: default_list_pipeline (referenced in run_smoke_tests.py)
resource "harness_platform_pipeline" "default_list_pipeline" {
  depends_on = [
    harness_time_sleep.tier_1
  ]
  identifier = "default_list_pipeline"
  name       = "default_list_pipeline"
  org_id     = harness_platform_organization.core.id
  project_id = harness_platform_project.core.id
  tags       = local.common_tags_tuple

  # Minimal pipeline YAML with a single shell script step
  yaml = <<-EOT
    pipeline:
      name: default_list_pipeline
      identifier: default_list_pipeline
      projectIdentifier: ${harness_platform_project.core.id}
      orgIdentifier: ${harness_platform_organization.core.id}
      tags:
        ${indent(4, yamlencode(local.common_tags))}
      stages:
        - stage:
            name: Test Stage
            identifier: test_stage
            type: Custom
            spec:
              execution:
                steps:
                  - step:
                      type: ShellScript
                      name: Echo
                      identifier: echo
                      spec:
                        shell: Bash
                        source:
                          type: Inline
                          spec:
                            script: echo "tf importer test"
      variables:
        - name: test
          type: String
          description: ""
          required: False
          value: <+input>
  EOT
}

# Pre-production environment for smoke tests (environments_v2.py)
# Identifier must match: default_list_environment (referenced in run_smoke_tests.py)
resource "harness_platform_environment" "default_list_environment" {
  depends_on = [
    harness_time_sleep.tier_1
  ]
  identifier = "default_list_environment"
  name       = "default_list_environment"
  org_id     = harness_platform_organization.core.id
  project_id = harness_platform_project.core.id
  type       = "PreProduction"
  tags       = local.common_tags_tuple
}

# Text secret for connector credentials (referenced by default_list_connector)
# Identifier must match: default_list_secret (referenced in run_smoke_tests.py)
# Stored in Harness' built-in secret manager (harnessSecretManager)
resource "harness_platform_secret_text" "default_list_secret" {
  identifier = "default_list_secret"
  name       = "default_list_secret"
  org_id     = harness_platform_organization.core.id
  project_id = harness_platform_project.core.id
  tags       = local.common_tags_tuple

  secret_manager_identifier = "harnessSecretManager"
  value_type                = "Inline"
  value                     = "secret"
}

# GitHub connector for smoke tests (connectors.py, workspace provisioning)
# Identifier must match: default_list_connector (referenced in run_smoke_tests.py)
# Waits for Tier 2 to ensure secrets are fully propagated
resource "harness_platform_connector_github" "default_list_connector" {
  depends_on = [
    harness_time_sleep.tier_2
  ]
  identifier = "default_list_connector"
  name       = "default_list_connector"
  org_id     = harness_platform_organization.core.id
  project_id = harness_platform_project.core.id
  tags       = local.common_tags_tuple

  url                = "https://github.com/account"
  connection_type    = "Account"
  validation_repo    = "some_repo"
  delegate_selectors = ["harness-delegate"]
  credentials {
    http {
      username  = "username"
      token_ref = harness_platform_secret_text.default_list_secret.id
    }
  }
}

# IACM (Infrastructure as Code Management) pipeline for workspace orchestration
# This pipeline defines stages for OpenTofu init, plan, approval, apply, and destroy
# Used by default_list_workspace as a default pipeline for workspace operations
resource "harness_platform_pipeline" "default_iacm_pipeline" {
  depends_on = [
    harness_time_sleep.tier_1
  ]
  identifier = "default_iacm_pipeline"
  name       = "default_iacm_pipeline"
  org_id     = harness_platform_organization.core.id
  project_id = harness_platform_project.core.id
  tags       = local.common_tags_tuple
  yaml       = <<-EOT
    pipeline:
      name: default_iacm_pipeline
      identifier: default_iacm_pipeline
      projectIdentifier: ${harness_platform_project.core.id}
      orgIdentifier: ${harness_platform_organization.core.id}
      tags:
        ${indent(4, yamlencode(local.common_tags))}
      stages:
        - stage:
            description: ""
            identifier: Provision
            name: Provision
            spec:
              execution:
                steps:
                  - step:
                      identifier: Generate_Provider_file
                      name: Generate Provider file
                      spec:
                        command: |
                          cd <+workspace.folderPath>
                          cat << EOF > providers.tf
                          terraform {
                            required_providers {
                              harness = {
                                source = "harness/harness"
                              }
                            }
                          }
                          provider "harness" {}
                          EOF
                          ls -l
                        shell: Sh
                      type: Run
                  - step:
                      identifier: init
                      name: init
                      spec:
                        command: init
                      timeout: 10m
                      type: IACMOpenTofuPlugin
                  - step:
                      identifier: plan
                      name: plan
                      spec:
                        command: plan
                      timeout: 10m
                      type: IACMOpenTofuPlugin
                  - step:
                      identifier: IACMApproval_1
                      name: IACMApproval_1
                      spec:
                        autoApprove: "false"
                      timeout: 1h
                      type: IACMApproval
                  - step:
                      identifier: apply
                      name: apply
                      spec:
                        command: apply
                      timeout: 10m
                      type: IACMOpenTofuPlugin
                  - step:
                      identifier: destroy
                      name: destroy
                      spec:
                        command: destroy
                      timeout: 10m
                      type: IACMOpenTofuPlugin
              platform:
                arch: Amd64
                os: Linux
              runtime:
                spec: {}
                type: Cloud
              workspace: <+input>
            tags: {}
            type: IACM
      variables: []

  EOT
}

# ============================================================================
# TIER 3: Advanced resources
# Workspaces, templates, input sets, and catalog entities
# Waits for Tier 3 to ensure all dependencies are ready
# ============================================================================

# OpenTofu workspace for IACM (Infrastructure as Code Management) smoke tests (workspaces.py)
# Identifier must match: default_list_workspace (referenced in run_smoke_tests.py)
# References GitHub connector for repository access and default IACM pipeline for operations
resource "harness_platform_workspace" "default_list_workspace" {
  depends_on = [
    harness_time_sleep.tier_3
  ]
  name                    = "default_list_workspace"
  identifier              = "default_list_workspace"
  org_id                  = harness_platform_organization.core.id
  project_id              = harness_platform_project.core.id
  provisioner_type        = "opentofu"
  provisioner_version     = "1.10.0"
  repository              = "https://github.com/org/repo"
  repository_branch       = "main"
  repository_path         = "tf/aws/basic"
  cost_estimation_enabled = true
  provider_connector      = harness_platform_connector_github.default_list_connector.id
  repository_connector    = harness_platform_connector_github.default_list_connector.id
  tags                    = local.common_tags_tuple

  # Terraform variable for workspace execution
  terraform_variable {
    key        = "key1"
    value      = "val1"
    value_type = "string"
  }

  # Map of operation types to pipelines for automated workspace management
  default_pipelines = {
    "destroy" = harness_platform_pipeline.default_iacm_pipeline.id
    "drift"   = harness_platform_pipeline.default_iacm_pipeline.id
    "plan"    = harness_platform_pipeline.default_iacm_pipeline.id
    "apply"   = harness_platform_pipeline.default_iacm_pipeline.id
  }
}

# ============================================================================
# TIER 3: IDP (Internal Developer Portal) resources
# Catalog entities, scorecard checks, and scorecards for IDP smoke tests
# ============================================================================

# IDP catalog entity for IDP smoke tests (entities.py)
# Identifier must match: default_idp_catalog_entity (referenced in run_smoke_tests.py)
resource "harness_platform_idp_catalog_entity" "default_idp_catalog_entity" {
  identifier = "default_idp_catalog_entity"
  org_id     = harness_platform_organization.core.id
  project_id = harness_platform_project.core.id
  kind       = "component"
  yaml       = <<-EOT
    apiVersion: harness.io/v1
    kind: Component
    type: service
    name: default_idp_catalog_entity
    identifier: "default_idp_catalog_entity"
    orgIdentifier: "${harness_platform_organization.core.id}"
    projectIdentifier: "${harness_platform_project.core.id}"
    owner: user:account/admin@harness.io
    spec:
        lifecycle: prod
    metadata:
        tags:
            - test
    EOT
}
# IDP scorecard check for quality assessment (scores.py)
# Identifier must match: default_idp_scorecard_check (referenced in run_smoke_tests.py)
# This check verifies that a repository contains a README.md file
resource "harness_platform_idp_scorecard_check" "default_idp_scorecard_check" {
  identifier        = "default_idp_scorecard_check"
  name              = "default_idp_scorecard_checks"
  description       = "Ensure the repository has a README file"
  rule_strategy     = "ALL_OF"
  default_behaviour = "FAIL"

  rules {
    data_source_identifier = "github"
    data_point_identifier  = "isFileExists"
    operator               = "=="
    value                  = "true"

    input_values {
      key   = "filePath"
      value = "README.md"
    }
  }
}

# IDP scorecard for baseline production quality metrics (scores.py)
# Identifier must match: default_idp_scorecard (referenced in run_smoke_tests.py)
# This scorecard applies the above check to component services and calculates weighted scores
resource "harness_platform_idp_scorecard" "default_idp_scorecard" {
  identifier         = "default_idp_scorecard"
  name               = "default_idp_scorecard"
  description        = "Baseline production quality scorecard"
  published          = true
  weightage_strategy = "EQUAL_WEIGHTS"

  filter {
    kind = "component"
    type = "service"
  }

  checks {
    identifier = harness_platform_idp_scorecard_check.default_idp_scorecard_check.identifier
    custom     = true
  }
}
