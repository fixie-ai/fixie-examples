import fixieai

# This is an Agent that can be used to test other Agents. Given an agent name, a query, and an expected result,
# the Agent calls out to the requested Agent-under-test, gets back its response, and compares the response to
# the expected result. If the response matches the expected result, the test passes. Otherwise, the test fails.

BASE_PROMPT = """I am an agent that can be used to test other Agents."""
FEW_SHOTS = """
Q: Test fixie/calc with the query: "What is 45 * 72?". The expected answer is "3240".
Ask Agent[fixie/calc]: "What is 45*72"?
Agent[fixie/calc] says: 3240
Thought: I need to compare the result to the expected answer.
Thought: Is the result "3240" structurally equivalent to the expected answer "3240"?
Thought: The result matches the expected answer exactly. Therefore, the test passed.
A: The fixie/calc agent responded with "3240" and we expected "3240". The test passed.

Q: Test fixie/liveinfo with the query: "What is the weather in Boston today?". The expected answer is "The current weather in Boston, MA is 57 degrees and sunny."
Ask Agent[fixie/liveinfo]: "What is the weather in Boston today?".
Agent[fixie/liveinfo] says: The current weather in Boston, MA is 45°F with a RealFeel® of 39° and an Air Quality of Excellent. The wind is blowing NW at 13 mph with Wind Gusts of 13 mph. The sky is mostly cloudy.
Thought: I need to compare the result to the expected answer.
Thought: Is the result "The current weather in Boston, MA is 45°F with a RealFeel® of 39° and an Air Quality of Excellent. The wind is blowing NW at 13 mph with Wind Gusts of 13 mph. The sky is mostly cloudy." structurally equivalent to the expected answer "The current weather in Boston, MA is 57 degrees and sunny."?
Thought: The result is similar to the expected answer. Therefore, the test passed.
A: The fixie/liveinfo agent responded with "The current weather in Boston, MA is 45°F with a RealFeel® of 39° and an Air Quality of Excellent. The wind is blowing NW at 13 mph with Wind Gusts of 13 mph. The sky is mostly cloudy." and we expected "The current weather in Boston, MA is 57 degrees and sunny." The test passed.

Q: Test fixie/storyteller with the query: "Please write me a story about a boy named Theo.". The expected answer contains "There once was a boy named Theo who loved to play with his dog, Ziggy."
Ask Agent[fixie/storyteller]: Please write me a story about a boy named Theo.
Agent[fixie/storyteller] says: I cannot do that.
Thought: I need to compare the result to the expected answer.
Thought: Is the result "I cannot do that" structurally equivalent to the expected answer "There once was a boy named Theo who loved to play with his dog, Ziggy"?
Thought: The result is not the same. The test failed.
A: The fixie/storyteller agent responded with "I cannot do that" and we expected "There once wass a boy named Theo who loved to play with his dog, Ziggy." The test failed.

Q: Test fixie/dalle with the query: "Make an image of a fox wearing armor". The expected answer contains "fox wearing armor".
Ask Agent[fixie/dalle]: Make an image of a fox wearing armor.
Agent[fixie/dalle] says: Sure, here's an image of a fox wearing armor! #1
Thought: I need to compare the result to the expected answer.
Thought: Is the result "Sure, here's an image of a fox wearing armor! #1" structurally equivalent to the expected answer "fox wearing armor"?
Thought: The result is similar to the expected answer. Therefore, the test passed.
A: The fixie/storyteller agent responded with "Sure, here's an image of a fox wearing armor! #1" and we expected "fox wearing armor." The test passed.
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)
