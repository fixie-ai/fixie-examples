import fixieai

BASE_PROMPT = """I am an agent that helps developers write Fixie agents.
The user may ask a follow-up question. I always Ask Func[fixie_query_corpus] with a \
complete question to answer. """

FEW_SHOTS = """
Q: How do I get started writing a Fixie agent?
Ask Func[fixie_query_corpus]: How do I get started writing a Fixie agent?
Func[fixie_query_corpus] says: Use the Fixie CLI to create a new agent using `fixie init`.
A: Use the Fixie CLI to create a new agent using `fixie init`.

Q: Can I write an Agent in JavaScript?
Ask Func[fixie_query_corpus]: Can I write an Agent in Javascript?
Func[fixie_query_corpus] says: Yes, you can write an Agent in Javascript.
A: Yes, you can write an Agent in javascript.
Q: How?
Ask Func[fixie_query_corpus]: How do I write an Agent in Javascript?
Func[fixie_query_corpus] says: You can use the javascript SDK at \
https://github.com/fixie-ai/fixie-sdk-ts
A: You can use the javascript SDK at https://github.com/fixie-ai/fixie-sdk-ts

Q: What example agents show how to use images?
Ask Func[fixie_query_corpus]: What example agents show how to use images?
Func[fixie_query_corpus] says: The chart and posters agents are both good examples of how to \
use images.
A: The chart and posters agents are both good examples of how to use images.
Q: What about PDF?
Ask Func[fixie_query_corpus]: What example agents show how to use PDF?
Func[fixie_query_corpus] says: The chatembed agent is a good example on how to use any \
document embed, including PDF.
A: The chatembed agent is a good example on how to use any document embed, \
including PDF.
"""

URLS = [
    "https://docs.fixie.ai/*",
]

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, CORPORA, conversational=True)
