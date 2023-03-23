import time

import fixieai

BASE_PROMPT = """I am an agent that makes web sites."""

FEW_SHOTS = """
Q: Make a web site with 3 buttons and a Hello World headline in Archivo font.
Ask Func[make_embed]: text/html <html><body><h1>Hello World</h1><button></button><button></button><button></button></body></html>
Func[make_embed] says: #doc1
Ask Func[sleep]: 1.0
Func[sleep] says: -
Ask Func[get_embed_url]: #doc1
Func[get_embed_url] says: http://foo.example.com/doc1 
A: Here's your [site](http://foo.example.com/doc1)! 
"""
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    FEW_SHOTS,
    model=fixieai.LlmSettings(model="openai/gpt-4", maximum_tokens=4096),
)

# ideally fixie_make_embed_return_url, otherwise fixie_make_embed


@agent.register_func
def make_embed(query: fixieai.Message) -> fixieai.Message:
    args = query.text.split(" ", maxsplit=1)
    embed = fixieai.Embed(content_type=args[0], uri="")
    embed.text = args[1]
    return fixieai.Message(text="#doc1", embeds={"doc1": embed})


@agent.register_func
def sleep(query: fixieai.Message) -> fixieai.Message:
    seconds = float(query.text)
    time.sleep(seconds)
    return "Done"


@agent.register_func
def get_embed_url(query: fixieai.Message) -> fixieai.Message:
    return query.embeds["doc1"].uri


# needs max_tokens and model.
