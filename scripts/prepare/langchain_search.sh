#!/usr/bin/env bash
set -eu -o pipefail

cat > $1/.env <<EOF
SERPAPI_API_KEY=$(gcloud secrets versions access --secret fixie-examples_langchain-search_serpapi-api-key latest)
EOF
