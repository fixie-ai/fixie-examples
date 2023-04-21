#!/usr/bin/env bash

set -eux -o pipefail

# This script deploys the agents in the Fixie Examples repo to Fixie.
# For each subdirectory in `agents`, it first checks to see if a `deploy.sh` file is present.
# If so, it runs that. Otherwise, it runs `fixieai deploy` on the agent directory.

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

    agent_name=$(basename $agent_dir)
    if [ -f scripts/prepare/${agent_name}.sh ]; then
        echo "Preparing $agent_name"
        scripts/prepare/${agent_name}.sh $agent_dir
    fi

    echo Deploying: $agent_dir
    fixieai deploy --public $agent_dir || echo "WARNING: Failed to deploy $agent_name"
done
