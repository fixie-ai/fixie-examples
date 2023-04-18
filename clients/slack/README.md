# Fixie Slack Bot

This is an example of a Slack App that acts as a Fixie client. When you install the app in a
Slack channel, you can say things like:
```
@Fixie What is Elon Musk tweeting about?
```
and Fixie will respond (in a thread) with the answer!

## Installation instructions

First, you need to navigate to the Slack Apps developer dashboard and create a new app.
Call it "Fixie" if you like.

https://api.slack.com/apps/

The App needs the Bots, Event Subscriptions, and Permissions features enabled.

Under **OAuth and Permissions**, ensure that you have added the following permissions:
* `app_mentions:read`
* `chat:write`

Under **Event Subscriptions** ensure that `app_mention` is listed under **Subscribe to
Bot Events**.

Create a `.env` file in this directory, containing the following:
```
SLACK_BOT_TOKEN=<Slack bot token>
SLACK_SIGNING_SECRET=<Slack signing secret>
FIXIE_API_KEY=<Fixie API key>
```

The `SLACK_BOT_TOKEN` can be obtained from the App's **OAuth and Permissions** page.

The `SLACK_SIGNING_SECRET` can be obtained from the App's **Basic Information** page.

Your `FIXIE_API_KEY` can be obtained from your Fixie user profile page.

## Deploying to Google Cloud Run

You can deploy the Slack App to any cloud provider, but use the following instructions
if you would like to use Google Cloud Run.

Edit the `Justfile` and change the following values at the top:
* Change the value of `DOCKER_REGISTRY` to the Google Cloud container registry you want to use.
* Change the value of `DOCKER_IMAGE` to the name of the Docker image name you want to use.
* Change the value of `GOOGLE_CLOUD_PROJECT` to the name of the Google Cloud Project you are using.

Next, build the Slack App and push it to Docker, by running `just docker-build`.

Finally, you can deploy it with `just deploy`.

The deploy script will print out the URL of the deployed app, like this:
```
Fixie Slack bot deployed to https://fixie-slackbot-pgaenaxiea-uc.a.run.app
```
Take this URL and paste it into the **Request URL** field in the App's **Event Subscriptions**
page on the Slack app dashboard.

Once this has been done, you should be up and running!

## Testing the app

You'll need to install the Fixie App to your Slack workspace. Once this has been done, you can
invite the Fixie App to a channel. Once in a channel, you can send it a message by directly
`@`-mentioning it, like so:
```
@Fixie What is the square root of 4941?
```