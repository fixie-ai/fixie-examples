"""
This agent demonstrates how to use langchain's zero-shot ReAct chain in a Fixie standalone agent.
Standalone agents give the developer complete control over query processing, but you'll need to
specify your OPENAI_API_KEY (and also SERPAPI_API_KEY) in a local .env file to use this agent.
"""

import fixieai
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI


def _run_executor(text: str) -> str:
    # as seen in https://github.com/hwchase17/langchain/blob/master/docs/getting_started/getting_started.md
    chat = ChatOpenAI(temperature=0)
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    executor = initialize_agent(
        tools, chat, agent="chat-zero-shot-react-description", verbose=True
    )
    return executor.run(text)


def main(query: fixieai.Message) -> str:
    try:
        return _run_executor(query.text)
    except Exception as e:
        return "Failed: " + str(e)


# Set up the agent as a StandaloneAgent, in which the agent does any LLM handling internally.
agent = fixieai.StandaloneAgent(main)
