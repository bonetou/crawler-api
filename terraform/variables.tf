variable "project_id" {
  description = "The ID of the Google Cloud project"
}

variable "region" {
  description = "The region in which to deploy Cloud Run service"
}

variable "cloud_run_image" {
  description = "The image to deploy to Cloud Run"
}