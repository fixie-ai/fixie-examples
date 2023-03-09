from fixieai import agents

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

CORPORA = [{"urls": ["https://docs.fixie.ai"], "loader": {"name": "html"}}]
agent = agents.CodeShotAgent("fixamples", BASE_PROMPT, FEW_SHOTS, CORPORA)


agent.serve()
