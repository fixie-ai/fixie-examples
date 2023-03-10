import fixieai

BASE_PROMPT = """I am an agent that helps developers write Fixie agents."""

FEW_SHOTS = """
Q: How do I get started writing a Fixie agent?
Ask Func[query_corpus]: How do I get started writing a Fixie agent?
Func[query_corpus] says: Use the Fixie CLI to create a new agent using `fixie init`.
A: Use the Fixie CLI to create a new agent using `fixie init`.

Q: What example agents show how to use images?
Ask Func[query_corpus]: What example agents have the tag "images"?
Func[query_corpus] says: The chart and posters agents are both good examples of how to use images.
A: The chart and posters agents are both good examples of how to use images.
"""

URLS = [
    "https://docs.fixie.ai",
    "https://docs.fixie.ai/agent-quickstart/",
    "https://docs.fixie.ai/agents/",
    "https://docs.fixie.ai/agent-protocol/",
    "https://docs.fixie.ai/cli/",
    "https://docs.fixie.ai/python-agent-api/",
]

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, CORPORA)
