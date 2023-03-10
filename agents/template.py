"""A templated Fixie agent!

Fixie docs:
    https://docs.fixie.ai

Fixie agent example:
    https://github.com/fixie-ai/fixie-examples
"""

import fixieai

BASE_PROMPT = """General info about what this agent does and the tone it should use."""

FEW_SHOTS = """
Q: Sample query to this agent
A: Sample response

Q: Another sample query
Ask Func[example]: input
Func[example] says: output
A: The other response is output
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def example(query: fixieai.Message) -> str:
    assert query.text == "input"
    return "output"
