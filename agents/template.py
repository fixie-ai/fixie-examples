"""Template Fixie agent."""

import random

import fixieai

BASE_PROMPT = """I am an agent that rolls a dice!"""

FEW_SHOTS = """
Q: Roll a dice!
Ask Func[dice]: 1
Func[dice] says: 4
A: You got a four!

Q: Roll two dices for me
Ask Func[dice]: 2
Func[dice] says: 6 6
A: You got two sixes! Feeling lucky.
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def dice(query: fixieai.Message) -> str:
    # Convert input string into an integer.
    num_dice = int(query.text.strip())
    # Roll the dice num_dice times.
    results = [str(random.randint(1, 6)) for _ in range(num_dice)]
    # Construct a simple string for LLM to consume.
    return " ".join(results)
