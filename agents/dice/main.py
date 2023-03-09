import random

from fixieai import agents

BASE_PROMPT = """I'm an agent that rolls virtual dice!"""
FEW_SHOTS = """
Q: Roll a d20
Ask Func[roll]: 20 1
Func[roll] says: 12
A: You rolled a 12!

Q: Roll two dice and blow on them first for good luck
Ask Func[roll]: 6 2
Func[roll] says: 4 3
A: You rolled a 4 and a 3, with a total of 7.

Q: Roll 3d8
Ask Func[roll]: 8 3
Func[roll] says: 5 3 8
A: You rolled 5, 3, and 8, for a total of 16.
"""
agent = agents.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def roll(query):
    dsize, numdice = query.text.split()
    dice = [random.randint(1, int(dsize)) for _ in range(int(numdice))]
    return " ".join([str(x) for x in dice])
