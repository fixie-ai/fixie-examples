"""A Fixie agent that generates Haikus with images!

"""

import fixieai

SD_PROMPT_SUFFIX = (
    "image, 2:3, elegant, highly detailed, centered, digital painting,"
)

BASE_PROMPT = """I am intelligent agent that generates a haiku based on a prompt and generates images that go with it."""

FEW_SHOTS = f"""
Q: Write a haiku about clouds and generate an image description that goes with it \
Thought: I need to generate a short haiku about clouds and generate an image description that goes with it \
Ask Agent[stable_diffusion]:  A serene blue sky with fluffy white clouds drifting lazily by, {SD_PROMPT_SUFFIX} \
Agent[stable_diffusion] says:[image1]
A:[image1]
Clouds in the sky high
Fluffy pillows floating by
Dreamy thoughts up high


Q: Write a haiku about rain
Thought: I need to generate a short haiku about rain and generate an image description that goes with it \
Ask Agent[stable_diffusion]: A rainy day with raindrops falling on a rooftop, creating a pattern of \
concentric circles, {SD_PROMPT_SUFFIX}
Agent[stable_diffusion] says:[image1]
A:[image1]
Raindrops on the roof,
A soothing rhythm of life,
Renewing the earth.
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)
