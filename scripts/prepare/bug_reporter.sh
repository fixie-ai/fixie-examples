#!/usr/bin/env bash
set -eu -o pipefail

cat > $1/.env <<EOF
GITHUB_ACCESS_TOKEN=$(gcloud secrets versions access --secret fixie-examples_bugreporter_github-access-token latest)
EOF
