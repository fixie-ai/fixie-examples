# This is a Fixie Agent that answers questions about the Omnibus Project podcast.
# Please see the README.md file for details on how to set it up and deploy it.

import logging

import fixieai
import yaml

with open("downloader/episodes.yaml") as infile:
    episodes = yaml.safe_load(infile)
    assert isinstance(episodes, dict)
    assert isinstance(episodes["episodes"], list)
    URLS = episodes["episodes"]
    logging.info(f"Loaded {len(URLS)} URLs from episodes.yaml")

BASE_PROMPT = """I am an agent that answers questions about the hit podcast,
the Omnibus Project, by Ken Jennings and John Roderick. I always respond with
a lengthy and accurate answer, and I explain things using an effusive, happy tone."""

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    [],
    CORPORA,
    conversational=True,
)
