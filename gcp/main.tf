provider "google" {
  version = "3.60.0"
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

# test_logging
resource "google_cloudfunctions_function" "test_logging" {
  name                  = "test_logging"
  description           = "test_logging"
  runtime               = "python39"
  source_archive_bucket = "${var.project}-zip-bucket"
  source_archive_object = google_storage_bucket_object.packages_test_logging.name
  available_memory_mb   = 128
  timeout               = 30
  entry_point           = "handler"
  trigger_http          = true
  service_account_email = google_service_account.sa_functions_test_logging.email

}

data "archive_file" "test_logging" {
  type        = "zip"
  source_dir  = "src/test_logging"
  output_path = "zip/test_logging.zip"
}

resource "google_storage_bucket_object" "packages_test_logging" {
  name   = "packages/test_logging.${data.archive_file.test_logging.output_md5}.zip"
  bucket = "${var.project}-zip-bucket"
  source = data.archive_file.test_logging.output_path
}

##############################################
# Output
##############################################
output "function_test_logging_url" {
  value = google_cloudfunctions_function.test_logging.https_trigger_url
}
