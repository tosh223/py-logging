version = latest

build-local:
	@docker build -t logging-run:${version} ./src/logging-run

build-gcr:
	@gcloud builds submit --tag gcr.io/${GCP_PROJECT}/logging-run ./src/logging-run

trigger:
	$(eval token=$(shell gcloud auth print-identity-token))
	@curl -H "Authorization: Bearer $(token)" ${LOGGING_RUN_URL}
