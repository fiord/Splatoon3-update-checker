variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "discord_token" {
  description = "Discord Bot Token"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Google Cloud Zone"
  type        = string
  default     = "us-central1-a"
}
