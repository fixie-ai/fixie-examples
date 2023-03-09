# Fixie Examples

This repo contains examples of how to use the Fixie.ai platform. You can clone this repository directly to get started.

Built a cool agent that you want to share? Contribute back to this repo by opening a PR!

## Installing the Fixie CLI

You'll need to install the Fixie CLI to run these examples. You'll need Python >= 3.9 installed.

Install the Fixie CLI with `pip install fixieai`. Once installed, run `fixie auth` to authenticate to the Fixie service. If you don't already have an account, you'll need to create one at app.fixie.ai.

## Building agents locally

Fixie makes it easy to build, test, and debug your agents locally. To build an agent you need two files:
* agentname.yaml
* main.py

In the `agentname.yaml` file you will have the following fields:

```markdown
handle: "Agent"
name: "Agent"
description: |
  The `Agent` serves the following function.

  Example queries:
    -Do this task for me.

more_info_url: "https://github.com/fixie-ai/fixie-examples"
entry_point: main:agent
public: false
```

In the `main.py` file you will have the following fields:

```python

from fixieai import agents
import urllib

BASE_PROMPT = """I am an intelligent agent that does xxx ."""

FEW_SHOTS = """
Q: Example question here
A: Example of answer here
"""

agent = agents.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)
```


## Deploying agents

Deploying agents will automatically upload your agent to the Fixie cloud and start serving it immediately on the platform.

Running `fixie agent deploy` will create (or update) the agent and upload your fewshots and functions to Fixie. 
Once you ran this command you can go to app.fixie.ai and test your new agent by calling it in the main chat with "@agentname". 



## Styleguide for agents
We recommend that you keep the agent handle and agent name consistent and capitalize it. See example below

```markdown
handle: "Dice"
name: "Dice"
description: |
  The `Dice` agent rolls virtual dice.

  Example queries:
    - Roll a d20.
    - Roll two dice and blow on them first for good luck
    - Roll 3d8
  Tags: func
more_info_url: "https://github.com/fixie-ai/fixie-examples"
entry_point: main:agent
public: false
```

