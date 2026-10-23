# Harness Platform provider configuration variables
# These variables control Harness API authentication and target environment.
# All variables fallback to environment variables if not explicitly provided.

variable "harness_platform_url" {
  type        = string
  description = "Harness Platform URL (e.g., https://app.harness.io). Falls back to HARNESS_ENDPOINT env var."
  default     = null
}

variable "harness_platform_account" {
  type        = string
  description = "Harness account ID (required for API authentication). Falls back to HARNESS_ACCOUNT_ID env var."
  default     = null
}

variable "harness_platform_key" {
  type        = string
  description = "Harness Platform API key for authentication (required). Falls back to HARNESS_PLATFORM_API_KEY env var."
  default     = null
  sensitive   = true
}

# Configure Harness provider with credentials from variables or environment
# For OpenTofu usage: all env vars work identically to terraform
provider "harness" {
  endpoint         = var.harness_platform_url
  account_id       = var.harness_platform_account
  platform_api_key = var.harness_platform_key
}
