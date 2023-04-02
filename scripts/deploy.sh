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
    echo Deploying: $agent_dir
    if [ -f $agent_dir/deploy.sh ]; then
        (cd $agent_dir && ./deploy.sh) || echo "WARNING: Failed to deploy $agent_dir"
    else
        fixieai deploy --no-validate --public $agent_dir || echo "WARNING: Failed to deploy $agent_dir"
    fi
done
