provider "google" {
  project = var.project_id
  region  = var.region
}


resource "google_cloud_run_v2_service" "crawler_api" {
  name     = "crawler-api"
  location = "us-central1"
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.cloud_run_image
      resources {
        limits = {
          cpu    = "2"
          memory = "1024Mi"
        }
      }
    }
  }
  traffic {
    percent = 100
  }
}

resource "google_pubsub_topic" "crawling_started_topic" {
  name = "crawling-started"
}

resource "google_pubsub_subscription" "crawling_started_subscription" {
  name   = "crawling-started-subscription"
  topic  = google_pubsub_topic.crawling_started_topic.name
  push_config {
    push_endpoint = "${google_cloud_run_v2_service.crawler_api.uri}/internal/process"
  }
}
