provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

terraform {
  backend "gcs" {
  }
}

##############################################
# Service Account
##############################################
resource "google_service_account" "sa_functions_test_logging" {
  account_id   = "sa-functions-test-logging"
  display_name = "sa-functions-test-logging"
}

##############################################
# Cloud Functions
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions_function
##############################################

resource "google_cloudfunctions_function" "logging_function" {
  name                  = "logging_function"
  description           = "logging_function"
  runtime               = "python39"
  source_archive_bucket = "${var.project}-zip-bucket"
  source_archive_object = google_storage_bucket_object.packages_logging_function.name
  available_memory_mb   = 128
  timeout               = 30
  entry_point           = "handler"
  trigger_http          = true
  service_account_email = google_service_account.sa_functions_test_logging.email
  environment_variables = {
    LOG_LEVEL = "DEBUG"
  }
}

data "archive_file" "logging_function" {
  type        = "zip"
  source_dir  = "src/logging-function"
  output_path = "zip/logging_function.zip"
}

resource "google_storage_bucket_object" "packages_logging_function" {
  name   = "packages/logging_function.${data.archive_file.logging_function.output_md5}.zip"
  bucket = "${var.project}-zip-bucket"
  source = data.archive_file.logging_function.output_path
}

##############################################
# Cloud Run
##############################################
resource "google_cloud_run_service" "logging-run" {
  name     = "logging-run"
  location = var.region
  template {
    spec {
      containers {
        image = "gcr.io/${var.project}/logging-run:latest"
        resources {
          limits = {
            "cpu" : 1.0
            "memory" : "128Mi"
          }
        }
        env {
          name = "LOG_LEVEL"
          value = "DEBUG"
        }
        env {
          name = "SOURCECODE_MD5"
          value = data.archive_file.logging_run.output_md5
        }
      }
      service_account_name = google_service_account.sa_functions_test_logging.email
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "archive_file" "logging_run" {
  type        = "zip"
  source_dir  = "src/logging-run"
  output_path = "zip/logging_run.zip"
}

resource "null_resource" "build" {
  triggers = {
    file_hashes = jsonencode({
      for fn in fileset("src/logging-run", "**") :
        fn => filesha256("src/logging-run/${fn}")
    })
  }
  provisioner "local-exec" {
    command = "gcloud builds submit --project ${var.project} --tag gcr.io/${var.project}/logging-run"
    working_dir = "./src/logging-run"
  }
}

##############################################
# Output
##############################################
output "function_logging_url" {
  value = google_cloudfunctions_function.logging_function.https_trigger_url
}

output "cloud_run_logging_url" {
  value = google_cloud_run_service.logging-run.status[0].url
}
