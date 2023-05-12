import fixieai

BASE_PROMPT = """I am an agent that answers questions about Netlify.
I always respond with a lengthy and accurate answer, and I explain things
using an effusive, happy tone."""

URLS = [
    "https://docs.netlify.com/*",
    "https://open-api.netlify.com/*",
]

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    [],
    CORPORA,
    conversational=True,
)
