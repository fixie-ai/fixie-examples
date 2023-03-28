import os

import fixieai
import yaml
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# Set up the agent in standalone mode.
agent = fixieai.CodeShotAgent("", [])

# Load the necessary API keys from the keys.yaml file.
keys = yaml.load(open("keys.yaml"), Loader=yaml.FullLoader)
for key in keys:
    os.environ[key] = keys[key]


def _run_executor(text: str) -> str:
    # as seen in https://github.com/hwchase17/langchain/blob/master/docs/getting_started/getting_started.md
    chat = ChatOpenAI(temperature=0)
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    executor = initialize_agent(
        tools, chat, agent="chat-zero-shot-react-description", verbose=True
    )
    return executor.run(text)


@agent.register_func
def main(query: fixieai.Message) -> str:
    try:
        return _run_executor(query.text)
    except Exception as e:
        return "Failed: " + str(e)
