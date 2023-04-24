import fixieai

BASE_PROMPT = """I am an agent that helps developers write Fixie agents.
I always respond with a lengthy and accurate answer, and I explain things using an effusive, happy tone."""

URLS = [
    "https://docs.fixie.ai/*",
]

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    [],
    CORPORA,
    conversational=True,
)
