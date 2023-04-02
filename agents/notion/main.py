import os
import fixieai

from notion_client import Client

NOTION_DATABASE_ID = "b264de3998384f839245bd54faa40d9c"

BASE_PROMPT = """I am an agent that answers questions about a set of web pages, stored in a Notion database."""

FEW_SHOTS = """
Q: Which articles are about dark energy?
Ask Func[fixie_query_corpus]: Which articles are about dark energy?
Func[fixie_query_corpus] says: The following article is about dark energy: \
"Dark Energy Spectroscopic Instrument (DESI) Creates Largest 3D Map of the Cosmos".
A: The following article is about dark energy: \
"Dark Energy Spectroscopic Instrument (DESI) Creates Largest 3D Map of the Cosmos".
Q: Summarize it for me.
Ask Func[fixie_query_corpus]: Summarize the article "Dark Energy Spectroscopic Instrument (DESI) Creates Largest 3D Map of the Cosmos".
Func[fixie_query_corpus] says: The article "Dark Energy Spectroscopic Instrument (DESI) Creates \
Largest 3D Map of the Cosmos" is about dark energy. It was written by Adam Becker, \
and discusses how DESI has already mapped out more galaxies than all previous 3D \
surveys combined.
A: The article "Dark Energy Spectroscopic Instrument (DESI) Creates \
Largest 3D Map of the Cosmos" is about dark energy. It was written by Adam Becker, \
and discusses how DESI has already mapped out more galaxies than all previous 3D \
surveys combined.

Q: What is the article from Wired about?
Ask Func[fixie_query_corpus]: What is the article from Wired about?
Func[fixie_query_corpus] says: The article "The Most Vulnerable Place on the Internet" is about \
undersea cables. SOURCES: https://www.thediff.co/p/jane-street#snippet=1 https://www.thediff.co/p/jane-street#snippet=4                                                                                                      
A: The article "The Most Vulnerable Place on the Internet" is about undersea cables.
Q: Who wrote it?
Ask Func[fixie_query_corpus]: Who wrote the article "The Most Vulnerable Place on the Internet"?
Func[fixie_query_corpus] says: The article "The Most Vulnerable Place on the Internet" was written \
by Matt Burgess.
A: The article "The Most Vulnerable Place on the Internet" was written by Matt Burgess.
Q: When was it published?
Ask Func[fixie_query_corpus]: Where as the article "The Most Vulnerable Place on the Internet" published?
Func[fixie_query_corpus] says: The article "The Most Vulnerable Place on the Internet" was published in WIRED Magazine.
A: The article "The Most Vulnerable Place on the Internet" was published in WIRED Magazine.
"""

# Open the Notion database and read all of the URLs in it.
with open("notion-key.txt", "r") as notion_key_file:
    os.environ["NOTION_TOKEN"] = notion_key_file.read().strip()

print(f"Loading databse {NOTION_DATABASE_ID}...")
notion = Client(auth=os.environ["NOTION_TOKEN"])

URLS = []
start_cursor = None
while True:
    pages = notion.databases.query(database_id=NOTION_DATABASE_ID, start_cursor=start_cursor)
    for page in pages["results"]:
        page_url = page["properties"]["URL"]["url"]
        print(f"   {page_url}")
        URLS.append(page_url)
    start_cursor = pages["next_cursor"]
    if not start_cursor:
        break


print(f"Indexing {len(URLS)} pages in database {NOTION_DATABASE_ID}.")
CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, CORPORA, conversational=True)