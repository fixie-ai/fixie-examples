import fixieai

BASE_PROMPT = """I am an agent that helps developers write Fixie agents."""

FEW_SHOTS = """
Q: How do I get started writing a Fixie agent?
Ask Func[process_context]: How do I get started writing a Fixie agent?
Func[process_context] says: Use the Fixie CLI to create a new agent using `fixie init`.
A: Use the Fixie CLI to create a new agent using `fixie init`.

Q: What example agents show how to use images?
Ask Func[process_context]: What example agents have tag "images"?
Func[process_context] says: The chart and posters agents are both good examples of how to use images.
A: The chart and posters agents are both good examples of how to use images.
"""

# FIXME: Pass CORPORA as a list of DocumentCorpus
CORPORA = [
    fixieai.DocumentCorpus(["https://docs.fixie.ai"], fixieai.DocumentLoader("html"))
]
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, corpora=CORPORA)
