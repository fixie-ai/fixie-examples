import os
import fixieai

from notion_client import Client

with open("notion-key.txt", "r") as notion_key_file:
    os.environ["NOTION_TOKEN"] = notion_key_file.read().strip()

notion = Client(auth=os.environ["NOTION_TOKEN"])

NOTION_DATABASE_ID = "b264de3998384f839245bd54faa40d9c"

print(f"Loading databse {NOTION_DATABASE_ID}...")
pages = notion.databases.query(database_id=NOTION_DATABASE_ID)
print(f"Found {len(pages['results'])} pages in database {NOTION_DATABASE_ID}.")
for page in pages["results"]:
    print("---------------------")
    page_title = page["properties"]["Title"]["title"][0]["plain_text"]
    page_url = page["properties"]["URL"]["url"]
    print(page_url + " - " + page_title)


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

# URLS = [
#     "https://docs.fixie.ai/*",
# ]

# CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
# agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, CORPORA)
