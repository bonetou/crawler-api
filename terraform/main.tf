provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_service" "crawler_api" {
  name     = "crawler-api"
  location = var.region
  template {
    spec {
      containers {
        image = var.cloud_run_image
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_pubsub_topic" "crawling_started_topic" {
  name = "crawling-started"
}

resource "google_pubsub_subscription" "crawling_started_subscription" {
  name   = "crawling-started-subscription"
  topic  = google_pubsub_topic.crawling_started_topic.name
  push_config {
    push_endpoint = "${google_cloud_run_service.crawler_api.status[0].url}/internal/process"
  }
}
