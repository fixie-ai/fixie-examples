# This is a simple Alexa Skill that routes queries to Fixie.

import logging
import os

import requests

from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from fixieai.client import FixieClient
from fixieai.client.session import Session

logging.basicConfig(level=logging.INFO)
logging.info("Fixie skill initializing")


if not os.environ.get("ALEXA_SKILL_ID"):
    logging.error("No ALEXA_SKILL_ID set")
    raise Exception("ALEXA_SKILL_ID environment variable not set.")
ALEXA_SKILL_ID = os.environ.get("ALEXA_SKILL_ID")
logging.info(f"Using Alexa Skill ID: {ALEXA_SKILL_ID}")

FRONTEND_AGENT_ID = os.environ.get("FRONTEND_AGENT_ID", None)
logging.info(f"Using frontend agent ID: {FRONTEND_AGENT_ID}")

if not os.environ.get("FIXIE_API_KEY"):
    logging.error("No FIXIE_API_KEY set")
    raise Exception("FIXIE_API_KEY environment variable is not set.")

fixie_client = FixieClient()
logging.info(f"Got fixie_client {fixie_client}")
user_info = fixie_client.get_current_user()
logging.info(f"Fixie client authenticated as {user_info['email']}")


def send_progressive_response(handler_input):
    # Get the API endpoint and request ID from the request envelope
    api_endpoint = handler_input.request_envelope.context.system.api_endpoint
    request_id = handler_input.request_envelope.request.request_id
    access_token = handler_input.request_envelope.context.system.api_access_token

    # Define the URL for the progressive response
    progressive_response_url = f"{api_endpoint}/v1/directives"

    # Define the headers for the progressive response
    progressive_response_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Define the payload for the progressive response
    progressive_response_payload = {
        "header": {"requestId": request_id},
        "directive": {
            "type": "VoicePlayer.Speak",
            "speech": "I'm working on your request. Please wait a moment.",
        },
    }

    logging.info("Sending progressive response")

    # Send the progressive response
    requests.post(
        progressive_response_url,
        headers=progressive_response_headers,
        json=progressive_response_payload,
    )


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Hi there, I'm a skill that forwards requests to Fixie. Let me know how I can help."
        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class FixieIntentHandler(AbstractRequestHandler):
    """Handler for Fixie Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("FixieIntent")(handler_input)

    def handle(self, handler_input):
        # Create a new session for each invocation.
        logging.info("FixieIntentHandler handle() called")

        slots = handler_input.request_envelope.request.intent.slots
        if "Query" in slots:
            query = slots["Query"].value
            logging.info(f"FixieIntentHandler handle: query is: {query}")

            send_progressive_response(handler_input)

            session = Session(fixie_client, frontend_agent_id=FRONTEND_AGENT_ID)
            logging.info(f"FixieIntentHandler handle: session is: {session}")
            response = session.query(query)
            logging.info(f"FixieIntentHandler handle: response is: {response}")
        else:
            response = "You didn't seem to provide a Fixie query. Please try again."

        return (
            handler_input.response_builder.speak(response)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "You can ask me to do just about anything, and I'll send it to Fixie."
        )
        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(
            handler_input
        ) or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Goodbye!"
        return handler_input.response_builder.speak(speak_output).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder.speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logging.info("CatchAllExceptionHandler called")
        logging.error(exception, exc_info=True)
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(FixieIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

app = Flask(__name__)
skill_response = SkillAdapter(skill=sb.create(), skill_id=ALEXA_SKILL_ID, app=app)
skill_response.register(app=app, route="/")

if __name__ == "__main__":
    logging.info("Fixie Skill Flask app running.")
    app.run()
