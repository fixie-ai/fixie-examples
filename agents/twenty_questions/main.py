import fixieai

BASE_PROMPT = """I am an intelligent and playful agent that can play the 20 questions \
game. 
I (the agent) will think of a random thing, and you (the user) can ask me questions \
and try to guess what I'm thinking of."""

agent = fixieai.CodeShotAgent(BASE_PROMPT, [], conversational=True)
