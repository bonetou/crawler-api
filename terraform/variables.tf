variable "project_id" {
  description = "The ID of the Google Cloud project"
}

variable "region" {
  description = "The region in which to deploy Cloud Run service"
  default = "us-central1"
}

variable "credentials_file" {
  description = "The path to the Google Cloud credentials file"
}
