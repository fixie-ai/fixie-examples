import fixieai

BASE_PROMPT = (
    """Hi, I'm a helpful chatbot who can answer questions from an uploaded file."""
)

FEW_SHOTS = """
Q: When did the thing happen? [text1]
Ask Func[query_embed]: When did the thing happen? [thing1]
Func[query_embed] says: It happened on March 1, 2023
A: The thing happened on March 1, 2023.

Q: What was the thing?
Ask Func[query_embed]: What was the thing? [text1]
Func[query_embed] says: The thing was a object.
A: The thing was a object.
"""

agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, conversational=True)
