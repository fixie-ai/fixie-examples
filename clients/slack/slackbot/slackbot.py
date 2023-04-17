"""This is an example Slack App that talks to Fixie."""

import logging
import os
import random
from typing import Dict


from fixieai.client import FixieClient
from fixieai.client.session import Session
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

logging.basicConfig(level=logging.INFO)


_THINKING_RESPONSES = [
    ":fox_face: Thinking...",
    ":fox_face: I'm on it!",
    ":fox_face: Working on it...",
    ":fox_face: Just a sec...",
    ":fox_face: Okay, gimme a minute...",
    ":fox_face: You got it!",
    ":fox_face: Hang tight!",
    ":fox_face: Okay, hang on a sec...",
]

# Be sure FIXIE_API_KEY is in your .env file.
fixie_client = FixieClient()

sessions: Dict[str, Session] = {}

# Be sure SLACK_BOT_TOKEN and SLACK_BOT_SIGNING_SECRET are in your .env file.
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@flask_app.route("/", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
    return handler.handle(request)


@app.event("app_mention")
def handle_mention(client, message, event, say):
    logging.info(f"handle_fixie_message called: {message}")
    say("Whassup!")

    channel = message["channel"]
    session = sessions.get(channel, None)
    if not session:
        # Create a new session for each channel.
        session = Session(fixie_client)
        sessions[channel] = session

    # Tell user that we're thinking.
    client.chat_postMessage(
        channel=message["channel"],
        user=message["user"],
        thread_ts=message.get("thread_ts", message["ts"]),
        text=random.choice(_THINKING_RESPONSES),
        reply_broadcast=False,
    )

    for message in session.run(message["text"]):
        logging.info(f"Got Fixie message: {message}")
        client.chat_postMessage(
            channel=event["channel"],
            thread_ts=event.get("thread_ts", event["ts"]),
            text=message,
            # TODO(mdw): Turn embeds into attachments.
            # attachments=out_attachments,
            reply_broadcast=False,
        )
