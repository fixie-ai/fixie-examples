# Fixie Examples

This repo contains examples of how to use the Fixie.ai platform. You can clone this repository directly to get started.

Built a cool agent that you want to share? Contribute back to this repo by opening a PR!

Full docs can be found here: [https://docs.fixie.ai/](https://docs.fixie.ai/).


## Installing the Fixie CLI

You'll need to install the Fixie CLI to run these examples. You'll need Python >= 3.9 installed.

Install the Fixie CLI with `pip install fixieai`. Once installed, run `fixie auth` to authenticate to the Fixie service. If you don't already have an account, you'll need to create one at app.fixie.ai.

## Building agents locally

You can scaffold out a default agent by running: `fixie init`

Fixie makes it easy to build, test, and debug your agents locally. To build an agent you need two files:
* `agent.yaml`
* `main.py`

In the `agent.yaml` file you will have the following fields:

```markdown
handle: "agent"
description: |
  The `agent` serves the following function.

  Example queries:
    -Do this task for me.

more_info_url: "https://github.com/fixie-ai/fixie-examples"
entry_point: main:agent
public: false
```

In the `main.py` file you will have the following fields:

```python

from fixieai import agents

BASE_PROMPT = """I am an intelligent agent that does a task."""

FEW_SHOTS = """
Q: Example question here
A: Example of answer here
"""

agent = agents.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)
```


## Deploying agents

Deploying agents will automatically upload your agent to the Fixie cloud and start serving it immediately on the platform.

Run `fixie agent deploy` to create (or update) the agent and upload your fewshots and functions to Fixie.

Once you run this command you test it locally by running the following command: `fixie session new '@username/agentname example query`.

Or you can go to app.fixie.ai and chat with your new agent by invoking it in the main chat with `@username/agentname`.



## Styleguide for agents
We recommend that you write the agent handle in small caps. See example below

```markdown
handle: "dice"
description: |
  The `dice` agent rolls virtual dice.

  Example queries:
    - Roll a d20.
    - Roll two dice and blow on them first for good luck
    - Roll 3d8
  Tags: func
more_info_url: "https://github.com/fixie-ai/fixie-examples"
entry_point: main:agent
public: false
```
