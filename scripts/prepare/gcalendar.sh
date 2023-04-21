#!/usr/bin/env bash
set -eu -o pipefail

gcloud secrets versions access --secret fixie_gcp_oauth_client_secret latest > $1/gcp-oauth-secrets.json
