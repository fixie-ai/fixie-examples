# ChatGPT Plugin for Fixie

This is a ChatGPT Plugin that routes requests to Fixie. It is very simple.
This runs as a Docker container on Google Cloud Run and accepts requests
from ChatGPT, which are then sent to agents in Fixie. You can use this in
ChatGPT to say things like:
```
Ask fixie/dalle to generate an image of a red fox wearing pajamas
```

## Setup and installation

First, create a file `.env` in this directory containing the following:
```
FIXIE_API_KEY=<Your Fixie API Key>
```
You can find this on your user profile page on https://app.fixie.ai.

Next, edit the `Justfile` and change the values of `DOCKER_REGISTRY`,
`DOCKER_IMAGE`, and `GOOGLE_CLOUD_PROJECT` at the top to your Docker
registry, image name, and GCP project name.

Next, run `just docker-build` which will build and push the Docker image.
You can then run `just deploy` which deploys the plugin to Google Cloud Run.
Note the URL of the Cloud Run deployed service, which will be used in the step
below.

## Using the Plugin with ChatGPT

In the ChatGPT web UI, at the top, go to 
**Plugins > Plugin Store > Install Unverified Plugin** and paste the URL of the
Cloud Run service into the box. This should cause the Plugin to be installed in
your ChatGPT session.
