import fixieai

BASE_PROMPT = (
    "Say hi to me, and I'll greet you in the persona of a random historical figure!"
)

agent = fixieai.CodeShotAgent(
    BASE_PROMPT, [], llm_settings=fixieai.LlmSettings(temperature=1.0)
)
