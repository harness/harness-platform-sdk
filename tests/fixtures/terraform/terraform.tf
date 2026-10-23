terraform {
  required_version = ">= 1.10.0, < 2.0.0"

  required_providers {
    # Harness Terraform provider: manages all platform resources (orgs, projects, pipelines, etc.)
    # Docs: https://registry.terraform.io/providers/harness/harness
    # Note: Compatible with OpenTofu as a drop-in replacement for terraform
    harness = {
      source  = "harness/harness"
      version = ">= 0.45"
    }
  }
}
