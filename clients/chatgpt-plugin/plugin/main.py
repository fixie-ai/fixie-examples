#!/usr/bin/env python3
# This is a simple ChatGPT Plugin that routes queries to Fixie.
#
# The idea is that one can ask the plugin about which agents are
# available, and then use ChatGPT to ask a question which ends up
# being sent to a specific agent, either explicitly (e.g., "Ask the fixie/dalle agent to
# generate an image of a cute fox") or implicitly (e.g., "Generate an image of a cute fox").

import json
import logging
import os

import flask
import flask_cors
from fixieai.client import FixieClient
from fixieai.client.session import Session

logging.basicConfig(level=logging.INFO)
logging.info(f"Fixie plugin initializing")

# Create the Flask app and configure CORS.
app = flask.Flask(__name__)
cors = flask_cors.CORS(app, origins=["https://chat.openai.com"])

# We need the FIXIE_API_KEY environment variable for our Fixie client.
if not os.environ.get("FIXIE_API_KEY"):
    logging.error("No FIXIE_API_KEY set")
    raise Exception("FIXIE_API_KEY environment variable is not set.")

# Initialize the Fixie client instance.
fixie_client = FixieClient()
logging.info(f"Got fixie_client {fixie_client}")
user_info = fixie_client.get_current_user()
logging.info(f"Fixie client authenticated as {user_info['email']}")


# This is invoked when the plugin wants to know the list of agents.
@app.get("/fixie/agents")
def get_agents():
    logging.info("get_agents called")
    agents = fixie_client.get_agents()
    agent_list = [
        {
            "agent": agent["agentId"],
            "name": agent["name"],
            "description": agent["description"],
        }
        for agent in agents.values()
    ]
    return flask.Response(response=json.dumps(agent_list), status=200)


# This is invoked when a given agent is to be sent a query.
@app.post("/fixie/agents/<string:username>/<string:agentname>")
def send_query(username, agentname):
    logging.info(f"send_query called: {username}/{agentname}")
    session = Session(fixie_client, frontend_agent_id=f"{username}/{agentname}")
    query = flask.request.json["query"]
    logging.info(f"send_query sending: {query}")
    response = session.query(query)
    logging.info(f"send_query got response: {response}")

    # We extract the embed URLs in the response and send them back to ChatGPT as "image URLs".
    # While these things may not, in fact, be images, this is usually the case and tricks ChatGPT
    # into rendering them directly in the ChatGPT UI.
    embeds = session.get_embeds()
    embed_urls = [embed["embed"]["url"] for embed in embeds]
    logging.info(f"send_query got embed_urls: {embed_urls}")
    query_response = json.dumps({"response": response, "image_urls": embed_urls})
    return flask.Response(query_response, status=200)


# The following handlers are boilerplate for the Plugin.
@app.get("/logo.png")
def plugin_logo():
    filename = "../logo.png"
    return flask.send_file(filename, mimetype="image/png")


@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
    with open("./ai-plugin.json") as f:
        text = f.read()
        return flask.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
def openapi_spec():
    with open("./openapi.yaml") as f:
        text = f.read()
        return flask.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
