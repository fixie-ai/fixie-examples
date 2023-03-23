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
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)

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
        with open("secret.txt") as f:
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
def question(query: fixieai.Message, user_storage: fixieai.UserStorage) -> str:
    print(f"Query: {query.text}")
    if not ready:
        if not initializing:
            init_thread = Thread(target=init)
            init_thread.start()
        return f"I am sorry, I can't answer that question right now. I am still initializing. Status: {status}"
    response = index.query(query.text)
    print(f"Response: {response}")
    return response.response
