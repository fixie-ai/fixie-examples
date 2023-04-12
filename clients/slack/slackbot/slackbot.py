"""This is an example Slack App that talks to Fixie."""

import logging
import random
from typing import Any, Dict
import os

from fixieai.client import FixieClient
from fixieai.client.session import Session
from slack_bolt import App

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


@app.message("Hey Fixie")
def handle_fixie_message(client, message, event, say):
    logging.info(f"handle_fixie_message called: {message}")

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


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
