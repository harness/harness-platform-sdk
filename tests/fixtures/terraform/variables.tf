# Feature flag to conditionally run additional fixture resources
# Set to true to provision resources defined in second.tf
variable "should_run_second" {
  type        = bool
  default     = false
  description = "Enable additional fixture resources (see second.tf). Useful for testing specific scenarios."
}
