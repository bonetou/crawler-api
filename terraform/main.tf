provider "google" {
  credentials = file(var.credentials_file)
  project = var.project_id
  region  = var.region
}

resource "google_pubsub_topic" "crawling_started_topic" {
  name = "crawling-started"
}

resource "google_pubsub_subscription" "crawling_started_subscription" {
  name   = "crawling-started-subscription"
  topic  = google_pubsub_topic.crawling_started_topic.name
  push_config {
    push_endpoint = "${var.cloud_run_url}/internal/process"
  }
  depends_on = [ google_pubsub_topic.crawling_started_topic ]
}
