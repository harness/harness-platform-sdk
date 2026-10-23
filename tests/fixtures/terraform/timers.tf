# Tiered sleep resources to enforce ordering of fixture provisioning
# These delays ensure API propagation between resource tiers, preventing race conditions
# when resources in higher tiers depend on lower tiers

# Foundation tier: waits for org and project creation before provisioning Tier 1 resources
resource "harness_time_sleep" "foundation" {
  depends_on = [
    harness_platform_organization.core,
    harness_platform_project.core,
  ]

  # Allow org/project APIs to fully propagate before proceeding to Tier 1
  create_duration = "10s"
}

# Tier 1: waits for foundation before provisioning pipelines, environments, secrets, connectors
resource "harness_time_sleep" "tier_1" {
  depends_on = [
    harness_time_sleep.foundation
  ]
  create_duration  = "5s"
  destroy_duration = "5s"
}

# Tier 2: waits for Tier 1 resources before provisioning secondary connectors/resources
resource "harness_time_sleep" "tier_2" {
  depends_on = [
    harness_time_sleep.tier_1,
  ]
  create_duration  = "5s"
  destroy_duration = "5s"
}

# Tier 3: waits for Tier 2 before provisioning advanced resources (workspaces, input sets, templates)
resource "harness_time_sleep" "tier_3" {
  depends_on = [
    harness_time_sleep.tier_2,
  ]
  create_duration  = "5s"
  destroy_duration = "5s"
}
