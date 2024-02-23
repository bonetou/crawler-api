variable "project_id" {
  description = "The ID of the Google Cloud project"
}

variable "region" {
  description = "The region in which to deploy Cloud Run service"
  default = "us-central1"
}

variable "cloud_run_url" {
  description = "The URL of the Cloud Run service"
}