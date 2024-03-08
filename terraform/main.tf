provider "google" {
  credentials = file(var.credentials_file)
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "images-repository" {
  location      = var.region
  repository_id = "images"
  description   = "A repository for storing images"
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "crawler-api" {
  name     = "crawler-api"
  location = var.region
  ingress = "INGRESS_TRAFFIC_ALL"

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

resource "google_pubsub_topic" "crawling_started_topic" {
  name = "crawling-started"
}

resource "google_pubsub_subscription" "crawling_started_subscription" {
  name   = "crawling-started-subscription"
  topic  = google_pubsub_topic.crawling_started_topic.name
  push_config {
    push_endpoint = "${google_cloud_run_v2_service.crawler-api.uri}/internal/extract_links"
  }
  depends_on = [ google_pubsub_topic.crawling_started_topic ]
}
