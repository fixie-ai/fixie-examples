"""A templated Fixie agent!

Fixie docs:
    https://docs.fixie.ai

Fixie agent example:
    https://github.com/fixie-ai/fixie-examples
"""

import fixieai
import requests

BASE_PROMPT = """I am a simple agent that allows the user to ask questions web a resource. 
I ask Func[load_doc] to load the resource from a url, and then always reach out to Func[fixie_query_embed] to
answer questions about the resource"""

FEW_SHOTS = """
Q: I want to ask questions about this resource: http://some_url
Ask Func[load_doc]: http://some_url
Func[load_doc] says: #doc1
A: I've finished reading the resource. Go ahead and ask me about it.
Q: Give me a short summary of this resource?
Ask Func[fixie_query_embed]: Give me a short summary of this resource #doc1
Func[fixie_query_embed] says: answer from the resource
A: answer from the resource

Q: tell me about https://some_url
Ask Func[load_doc]: https://some_url
Func[load_doc] says: #doc1
Ask Func[fixie_query_embed]: Give me a short summary of this resource #doc1
Func[fixie_query_embed] says: summary from the resource
A: I've finished reading the resource. 
Here is a short summary: 
    summary from resource, indented from the main response. 
Go ahead and ask me about it.
Q: Give me a short summary of this resource?
Ask Func[fixie_query_embed]: Give me a short summary of this resource #doc1
Func[fixie_query_embed] says: answer from the resource
A: answer from the resource
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, conversational=True)

@agent.register_func
def load_doc(query: fixieai.agents.Message) -> fixieai.Message:
    url = query.text
    response = requests.get(url)
    content_type = response.headers["Content-Type"]
    return fixieai.Message("#doc1", embeds={"doc1": fixieai.Embed(content_type, url)})

