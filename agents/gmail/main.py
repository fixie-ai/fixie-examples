import json
import random
from typing import Optional
from threading import Thread

import fixieai
from llama_index import GPTSimpleVectorIndex, download_loader

import os

BASE_PROMPT = """I'm an agent that answers questions about Gmail messages."""
FEW_SHOTS = """
Q: What are the next steps with Oana from SignalFire?
Ask Func[question]: What are the next steps with Oana from SignalFire?
Func[question] says: The next steps with Oana from SignalFire are to schedule a meeting for the week of March 20th.
A: The next steps with Oana from SignalFire are to schedule a meeting for the week of March 20th.

Q: What is Nick's start date?
Ask Func[question]: What is Nick's start date?
Func[question] says: Nick Heiner's start date is April 4.
A: Nick Heiner's start date is April 4.
"""

# Configure OAuth params.
with open("credentials.json") as f:
    credentials = json.load(f)["installed"]
oauth_params = fixieai.OAuthParams(
    client_id=credentials["client_id"],
    auth_uri=credentials["auth_uri"],
    token_uri=credentials["token_uri"],
    client_secret=credentials["client_secret"],
    scopes=["https://www.googleapis.com/auth/gmail.readonly"],
)

# Initialize agent.
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, oauth_params=oauth_params)

initializing = False
ready = False
status = "Initializing"
index: Optional[GPTSimpleVectorIndex] = None


def init() -> str:

    global initializing, ready, status, index
    if initializing:
        return
    try:
        initializing = True
        print("Initializing...")
        status = "Initializing..."
        with open("openaikey.txt") as f:
            line = f.readline()
            os.environ["OPENAI_API_KEY"] = line.strip()
        print("Downloading GmailReader...")
        status = "Downloading GmailReader..."
        GmailReader = download_loader("GmailReader")
        loader = GmailReader(query="label:inbox")
        print("Loading data...")
        status = "Loading data..."
        documents = loader.load_data()
        print("Building index...")
        status = "Building index..."
        index = GPTSimpleVectorIndex(documents)
        print("Ready")
        status = "Ready"
        ready = True
    except Exception as e:
        print(e)
        status = f"Gmail agent failed to initialize: {e}"
        ready = False
    finally:
        initializing = False


@agent.register_func
def question(
    query: fixieai.Message,
    user_storage: fixieai.UserStorage,
    oauth_handler: fixieai.OAuthHandler,
) -> str:
    print(f"Query: {query.text}")
    user_token = oauth_handler.user_token()
    if user_token is None:
        # Return the URL that the user should click on to authorize the Agent.
        return oauth_handler.get_authorization_url()

    if not ready:
        if not initializing:
            # The Llamahub GmailReader expects to find the token in the file `token.json`.
            with open("token.json", "w") as f:
                json.dump(user_token, f)
            # Run initialization in a separate thread since it can take a while to complete.
            init_thread = Thread(target=init)
            init_thread.start()
        return f"I am sorry, I can't answer that question right now. I am still initializing. {status}"
    response = index.query(query.text)
    print(f"Response: {response}")
    return response.response
