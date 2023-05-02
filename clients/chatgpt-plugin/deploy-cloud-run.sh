#!/usr/bin/env bash

set -eux -o pipefail

# This script deploys the Slack bot to Google Cloud Run.
# Invoke with:
#   deploy-cloud-run.sh <docker image name and tag> <google cloud project ID>

DOCKER_IMAGE=$1
export GOOGLE_CLOUD_PROJECT=$2

# Cloud Run instance hardware requirements.
GOOGLE_CLOUD_REGION="us-central1"
GOOGLE_CLOUD_RUN_CPU=4
GOOGLE_CLOUD_RUN_MEMORY=16Gi
GOOGLE_CLOUD_RUN_CONCURRENCY=80
# Number of instances to run.
MIN_INSTANCES="1"
# Name of the Google Cloud Run environment.
ENVIRONMENT_NAME="fixie-slackbot"

gcloud run services delete ${ENVIRONMENT_NAME} --region ${GOOGLE_CLOUD_REGION} --quiet || echo "Service not running - cannot delete"

# Create a service.yaml file for the Cloud Run service.
SERVICE_YAML=$(mktemp)
cat > $SERVICE_YAML <<EOF
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: ${ENVIRONMENT_NAME}
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "${MIN_INSTANCES}"
    spec:
      containerConcurrency: ${GOOGLE_CLOUD_RUN_CONCURRENCY}
      containers:
      - image: ${DOCKER_IMAGE}
        resources:
          limits:
            cpu: "${GOOGLE_CLOUD_RUN_CPU}"
            memory: "${GOOGLE_CLOUD_RUN_MEMORY}"
        env:
          - name: SLACK_BOT_TOKEN
            value: ${SLACK_BOT_TOKEN}
          - name: SLACK_SIGNING_SECRET
            value: ${SLACK_SIGNING_SECRET}
          - name: FIXIE_API_KEY
            value: ${FIXIE_API_KEY}
EOF

echo "Deploying to Cloud Run..."
gcloud run services replace ${SERVICE_YAML} --region ${GOOGLE_CLOUD_REGION}

# Ensure the service is made public.
gcloud run services add-iam-policy-binding ${ENVIRONMENT_NAME} \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region ${GOOGLE_CLOUD_REGION}

CLOUDRUN_SERVICE_URL=$(gcloud run services describe ${ENVIRONMENT_NAME} --region ${GOOGLE_CLOUD_REGION} --format "value(status.url)" || echo "")
echo "Fixie Slack bot deployed to ${CLOUDRUN_SERVICE_URL}"
exit 0