provider "google" {
  credentials = file(var.credentials_file)
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "images_repository" {
  location      = var.region
  repository_id = "images"
  description   = "A repository for storing images"
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "crawler_api" {
  name     = "crawler-api"
  location = var.region
  
  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
      resources {
        limits = {
          cpu    = "1"
          memory = "1024Mi"
        }
      }
    }
  }
}
  
  
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers"
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_v2_service.crawler_api.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

resource "google_pubsub_topic" "crawling_started_topic" {
  name = "crawling-started"
}

resource "google_storage_bucket" "crawling_screenshots" {
  name = "crawling-screenshots"
  location = var.region
  force_destroy = true
}


resource "google_pubsub_subscription" "crawling_started_subscription" {
  name   = "crawling-started-subscription"
  topic  = google_pubsub_topic.crawling_started_topic.name
  push_config {
    push_endpoint = "${google_cloud_run_v2_service.crawler_api.uri}/internal/extract_links"
  }
  depends_on = [ google_pubsub_topic.crawling_started_topic ]
}
