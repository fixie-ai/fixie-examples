#!/usr/bin/env bash

set -eu -o pipefail

# This script deploys the agents in the Fixie Examples repo to Fixie.

# Avoid revealing secret in logs.
set +x
gcp_oauth_secret=$(gcloud secrets versions access --secret fixie_gcp_oauth_client_secret latest || echo "NONE")

if [ ${gcp_oauth_secret} == "NONE" ]; then
  echo "Unable to deploy gcalendar agent. Unable to load secret: fixie_gcp_oauth_client_secret"
  exit 0
fi

echo ${gcp_oauth_secret} > gcp-oauth-secrets.json

set -x
fixieai deploy --no-validate --public .