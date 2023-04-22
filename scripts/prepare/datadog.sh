#!/usr/bin/env bash
set -eu -o pipefail

cat > $1/.env <<EOF
$(gcloud secrets versions access --secret fixie-examples_datadog_env latest)
EOF