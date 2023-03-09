# Fixie Examples

This repo contains examples of how to use the Fixie.ai platform. You can clone this repository directly to get started.

Built a cool agent that you want to share? Contribute back to this repo by opening a PR!

## Installing the Fixie CLI

You'll need to install the Fixie CLI to run these examples. You'll need Python >= 3.9 installed.

Install the Fixie CLI with `pip install fixieai`. Once installed, run `fixie auth` to authenticate to the Fixie service. If you don't already have an account, you'll need to create one at app.fixie.ai.

## Building agents locally

Fixie makes it easy to build, test, and debug your agents locally.

Run `fixie agent serve` from with an agent directory to connect your local agent with the Fixie platform.

## Deploying agents

Deploying agents will automatically upload your agent to the Fixie cloud and start serving it immediately on the platform.

Running `fixie agent deploy` will create (or update) the agent and upload your fewshots and functions to Fixie.
