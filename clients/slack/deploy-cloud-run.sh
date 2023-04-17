#!/usr/bin/env bash

set -eux -o pipefail

# This script deploys the Slack bot to Google Cloud Run.

# The base Google Cloud project we are running in.
export GOOGLE_CLOUD_PROJECT="fixie-frame"

# Cloud Run instance hardware requirements.
GOOGLE_CLOUD_RUN_CPU=4
GOOGLE_CLOUD_RUN_MEMORY=16Gi
GOOGLE_CLOUD_RUN_CONCURRENCY=80

# The Docker image to deploy. Tag is specified using the --image-tag argument.
DOCKER_IMAGE="us-central1-docker.pkg.dev/fixie-frame/fixie-frame/fixie-slackbot:latest"

MIN_INSTANCES="1"

ENVIRONMENT_NAME="fixie-slackbot"

CLOUDRUN_SERVICE_URL=$(gcloud run services describe ${ENVIRONMENT_NAME} --region us-central1 --format "value(status.url)" || echo "")

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
gcloud run services replace ${SERVICE_YAML} --region us-central1

# Ensure the service is made public.
gcloud run services add-iam-policy-binding ${ENVIRONMENT_NAME} \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region us-central1

echo "Fixie Slack bot deployed to ${CLOUDRUN_SERVICE_URL}"
exit 0
