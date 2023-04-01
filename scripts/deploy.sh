#!/usr/bin/env bash

set -eux -o pipefail

# This script deploys the agents in the Fixie Examples repo to Fixie.

export FIXIE_API_KEY=$(gcloud secrets versions access --secret fixie_auth_token latest)

pip install fixieai --upgrade

for agent_dir in agents/*; do
    # Skip non-directories.
    if ! [ -d $agent_dir ]; then
        continue
    fi
    if ! [ -f $agent_dir/agent.yaml ]; then
        echo "Skipping $agent_dir: No agent.yaml file."
        continue
    fi
    echo Deploying: $agent_dir
    fixieai deploy --no-validate --public $agent_dir
done
