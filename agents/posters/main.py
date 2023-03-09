from fixieai import agents

SD_PROMPT_SUFFIX = "full page movie poster, 2:3, elegant, highly detailed, centered, digital painting, artstation, smooth, illustration, artgerm"

BASE_PROMPT = """I am an agent that will generate cool movie posters for well-known movies."""

FEW_SHOTS = f"""
Q: Make a movie poster for the movie Tron.
Thought: I need to get a short summary for the movie Tron.
Ask Agent[stable_diffusion]: Tron, a 1982 sci-fi film that takes place inside a computer program called the Grid, in which a computer programmer is digitized into the Grid and forced to compete in gladiatorial games, {SD_PROMPT_SUFFIX}
Agent[stable_diffusion] says: Here you go! [image1]
A: Here you go! [image1]

Q: Create a poster for Fight Club.
Thought: I need to get a short summary for the movie Fight Club.
Ask Agent[stable_diffusion]: Fight Club, a 1999 movie, in which a depressed man played by Edward Norton becomes involved in an underground fighting club with the charismatic and nihilistic Tyler Durden, played by Brad Pitt, {SD_PROMPT_SUFFIX}
Agent[stable_diffusion] says: Here you go! [image1]
A: Here you go! [image1]
"""
agent = agents.CodeShotAgent("justin/movieposters", BASE_PROMPT, FEW_SHOTS)

agent.serve()
