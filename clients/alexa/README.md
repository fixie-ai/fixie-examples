# Alexa Skill for Fixie

This is an example Alexa Skill that talks to a Fixie Agent.
The idea here is to make it easy to take a given Fixie Agent and expose
it to Alexa users as a Skill.

To use the Skill, you would say something like, "Alexa, ask the Fixie Twitter agent
what is Barack Obama tweeting about?"

This is definitely a work in progress and does not work very well just yet.
The biggest challenge is that Alexa seems to have a hard timeout of about 8 seconds
on the response from the Skill, even if a progressive response is sent back.
Because most Fixie interactions take longer than this -- due to LLM processing overhead --
many queries will tend to exceed the timeout, resulting in an error on the Alexa end.

## Setup

First, you will need to install and configure the
[Alexa Skills Kit CLI tool](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html).
This requires setting up an Amazon developer account, an AWS IAM user, and running
`ask configure` to configure the CLI tool with the appropriate credentials.

Second, you need to create your Skill in the Alexa Developer Console.
We are not going to use the ASK CLI to create and configure the Skill, because
the Skill is itself not being deployed via ASK. Instead, you'll create the Skill
and configure it by hand in the Alexa Developer Console.

(Note that it should be possible to automate this process via the `ask smapi` commands,
however, I have not yet gotten around to doing this. Sorry for the extra work.)

You will want to create a new "Custom" Skill on the Alexa Developer Console. For the
interaction model, you can upload [this JSON file](skill-package/interactionModels/custom/en-US.json)
which defines a single intent, `FixieIntent`, with a single slot, `Query`, which is
used to populate the query sent to Fixie. Of course, feel free to tweak the interaction model
if you like.

We are using the invocation name "Fixie App" for this Skill, however,
you are free to use whatever invocation name you like.

We also use `just` and `poetry` as development tools for this skill, which you can install
from here:
* https://github.com/casey/just
* https://python-poetry.org/

## Building and Deploying the Skill

First, you need to create a file in this directory called `.env` containing
the following:
```
FIXIE_API_KEY=<your Fixie API key>
ALEXA_SKILL_ID=<your Alexa Skill ID>
FRONTEND_AGENT_ID=<Fixie Agent ID for the frontend agent to use>
```

The `FIXIE_API_KEY` is found on your Fixie user profile page on https://app.fixie.ai.

The `ALEXA_SKILL_ID` is found on the [Alexa Developer Dashboard](https://developer.amazon.com/alexa/console/ask).

The `FRONTEND_AGENT_ID` is the ID of the Fixie Agent you want the skill to send queries
to. To allow the skill to send queries to any agent, you can use the value
`fixie/fixie`. Normally, however, it's best to only select a single Agent, so this
could be something like `fixie/twitter` or `fixie/search`.

The code for the Skill is [`fixieskill.py`](fixieskill/fixieskill.py). It is using the
Python packages `ask-sdk-core`, `ask-sdk-webservice-support`, and `flask-ask-sdk`.
The Fixie client interface comes from the `fixieai` package.

Ideally, this Skill would be deployed as an AWS Lambda and deployed using `ask deploy`.
Unfortunately, I've found this does not work if you are developing on an Apple Silicon
Mac, since the wrong versions of several Python packages end up being used locally, which
are incompatible with the Lambda environment. To work around, this we are building the skill
as a Docker container, and end up deploying it to Google Cloud Run. This could just as well
be run on AWS Fargate, for example.

To build the Docker container, first edit `Justfile` and set the `DOCKER_REGISTRY`
and `DOCKER_IMAGE` variables to the Docker registry and image name you want to use.
Then run:
```bash
$ just docker-build
```
This will build a Docker container with the skill and all of its dependencies.

To deploy the container, first edit `Justfile` and set the `GOOGLE_CLOUD_PROJECT`
variable to the name of your Google Cloud project. Then run:
```bash
$ just deploy
```
This will deploy the container to Google Cloud Run.

Take note of the URL that is printed out after the container is deployed. You will
need to go to the Alexa Developer Console and configure the Endpoint for your model
to this URL using the `HTTPS` endpoint type. For the certificate type, select
the option `My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority`.

## Testing the Skill

Once the skill is deployed, you should be able to send it queries using `ask dialog`,
for example:
```
$ ask dialog --skill-id ${ALEXA_SKILL_ID}

User  > ask fixie app to tell me a joke about chickens
Alexa > 
Alexa > Why did the chicken cross the playground? To get to the other slide!
User  > 
```