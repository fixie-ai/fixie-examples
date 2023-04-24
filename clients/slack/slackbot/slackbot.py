"""This is an example Slack App that talks to Fixie."""

import logging
import os
import random
from typing import Dict

from fixieai.client import FixieClient
from fixieai.client.session import Session
from flask import Flask
from flask import request
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
def handle_mention(client, event, say):
    logging.info(f"handle_mention called: {event}")
    try:
        channel = event["channel"]
        session = sessions.get(channel, None)
        if not session:
            # Create a new session for each channel.
            session = Session(fixie_client)
            sessions[channel] = session

        # Tell user that we're thinking.
        client.chat_postMessage(
            channel=event["channel"],
            user=event["user"],
            thread_ts=event.get("thread_ts", event["ts"]),
            text=random.choice(_THINKING_RESPONSES),
            reply_broadcast=False,
        )

        for message in session.run(event["text"]):
            logging.info(f"Got Fixie message: {message}")
            text = message["text"]
            if "sentBy" in message and "handle" in message["sentBy"]:
                sentBy = message["sentBy"]["handle"] + ": "
            else:
                sentBy = ""

            client.chat_postMessage(
                channel=event["channel"],
                thread_ts=event.get("thread_ts", event["ts"]),
                text=f"{sentBy}{text}",
                # TODO(mdw): Turn embeds into attachments.
                # attachments=out_attachments,
                reply_broadcast=False,
            )

    except Exception as e:
        say(f"Sorry, I got an exception handling your query: {e}")
        say(e)
