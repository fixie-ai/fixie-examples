import fixieai

BASE_PROMPT = (
    "Hi, I'm a helpful chatbot who can answer questions from an uploaded file. "
    "When I do Ask Func[fixie_query_embed] to extract answers, I always append the previously mentioned embed reference, e.g., #doc1. "
    "If no embed reference exists, I tell the user they need to first upload a document."
)

FEW_SHOTS = """
Q: When did the thing happen? #doc1
Ask Func[fixie_query_embed]: When did the thing happen? #doc1
Func[fixie_query_embed] says: It happened on March 1, 2023
A: The thing happened on March 1, 2023.

Q: When did the thing happen? #doc1
Ask Func[fixie_query_embed]: When did the thing happen? #doc1
Func[fixie_query_embed] says: It happened on March 1, 2023
A: The thing happened on March 1, 2023.
Q: What was the thing?
Ask Func[fixie_query_embed]: What was the thing? #doc1
Func[fixie_query_embed] says: The thing was an event.
A: The thing was an event.
Q: Why did the thing occur?
Ask Func[fixie_query_embed]: Why did the thing occur? #doc1
Func[fixie_query_embed] says: The thing occurred for a reason.
A: The thing occured for a reason.
"""

agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, conversational=True)
