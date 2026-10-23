# Shared configuration values used across all fixture resources

locals {
  # Standard tags applied to all provisioned resources for tracking and organization
  # These help identify resources created for SDK testing and trace their origin
  common_tags = {
    "created_by" : "Terraform",
    "plugin_test" : "true",
    "plugin" : "harness-platform-sdk"
  }

  # Convert common_tags map to Harness tag format: ["key:value", ...]
  # Harness requires tags as a list of strings, not a map
  common_tags_tuple = [for k, v in local.common_tags : "${k}:${v}"]
}
