#!/usr/bin/env bash
set -eu -o pipefail

cat > $1/.env <<EOF
TWITTER_BEARER_TOKEN=$(gcloud secrets versions access --secret fixie-examples_twitter_twitter-bearer-token latest)
EOF
