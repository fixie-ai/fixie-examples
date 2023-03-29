import os
import fixieai

from notion_client import Client

with open("notion-key.txt", "r") as notion_key_file:
    os.environ["NOTION_TOKEN"] = notion_key_file.read().strip()

notion = Client(auth=os.environ["NOTION_TOKEN"])

PAGE_ID = "910f30d459cc4c4ca0d087c70aef2f32"

BASE_PROMPT = """I am an agent that answers questions from a knowledge base stored in Notion."""

FEW_SHOTS = """
Q: How do I get started writing a Fixie agent?
Ask Func[fixie_query_corpus]: How do I get started writing a Fixie agent?
Func[fixie_query_corpus] says: Use the Fixie CLI to create a new agent using `fixie init`.
A: Use the Fixie CLI to create a new agent using `fixie init`.

Q: What example agents show how to use images?
Ask Func[fixie_query_corpus]: What example agents have the tag "images"?
Func[fixie_query_corpus] says: The chart and posters agents are both good examples of how to \
use images.
A: The chart and posters agents are both good examples of how to use images.
"""

URLS = [
    "https://docs.fixie.ai/*",
]

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, CORPORA)
