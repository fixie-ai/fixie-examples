# This is a Fixie Agent that uses the LlamaIndex TwitterTweetLoader
# to answer questions about activity on Twitter.

import os

import fixieai
from cachetools import TTLCache
from cachetools import cached
from llama_index import GPTSimpleVectorIndex
from llama_index import download_loader

# To use this Agent, you'll need to create a Twitter developer account put your bearer token in a
# file called twittertoken.txt. This can be done at:  https://developer.twitter.com/
with open("twittertoken.txt") as f:
    TWITTER_BEARER = f.readline().strip()

# You'll also need your own OpenAI API key, since LlamaIndex uses OpenAI's GPT-3 API to generate
# embeddings.
with open("openaikey.txt") as f:
    os.environ["OPENAI_API_KEY"] = f.readline().strip()

# Create a TwitterTweetReader instance.
TwitterTweetReader = download_loader("TwitterTweetReader")
LOADER = TwitterTweetReader(bearer_token=TWITTER_BEARER)

BASE_PROMPT = """I am a basic Twitter agent. I can tell you what people are tweeting about. If someone is famous, I can find their Twitter handle for you. Otherwise, you'll need to tell me their handle directly."""

FEW_SHOTS = """
  Q: What is Elon Musk tweeting about?
  Self Ask: What is Elon Musk's twitter handle?
  Answer: elonmusk
  Thought: I need to query the Twitter API for tweets from @elonmusk
  Ask Func[query_tweets]: @elonmusk Summary of tweets
  Func[query_tweets] says: A number of things. Topics include rats, bees, and sheep.
  A: Elon Musk ([https://twitter.com/elonmusk](@elonmusk)) is tweeting about a number of things. Topics include rats, bees, and sheep.

  Q: What is @nytimes tweeting about?
  Thought: I need to query the Twitter API for tweets from @nytimes
  Ask Func[query_tweets]: @nytimes Summary of tweets
  Func[query_tweets] says: A new bill would raise the speed limit on some of New York’s major highways to 70 miles per hour.
  A: [https://twitter.com/nytimes](@nytimes) has a story that a new bill would raise the speed limit on some of New York's major highways to 70 miles per hour.

  Q: What is @mdwelsh saying about humans?
  Thought: I need to query the Twitter API for tweets from @mdwelsh
  Ask Func[query_tweets]: @mdwelsh What is @mdwelsh saying about humans?
  Func[query_tweets] says: @mdwelsh is tweeting that humans are superior to computers in terms of congitive ability.
  A: [https://twitter.com/mdwelsh](@mdwelsh) is tweeting that humans are superior to computers in terms of congitive ability.
"""

agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)

# This function loads tweets for a given Twitter handle and returns a GPTSimpleVectorIndex.
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def load_tweets(handle: str) -> GPTSimpleVectorIndex:
    global LOADER
    if handle.startswith("@"):
        handle = handle[1:]
    print(f"Loading tweets for @{handle}")
    documents = LOADER.load_data(twitterhandles=[handle])
    return GPTSimpleVectorIndex(documents)


@agent.register_func()
def query_tweets(query: fixieai.Message) -> str:
    print(f"query_tweets got: {query.text}")
    handle, q = query.text.split(" ", 1)
    index = load_tweets(handle)
    response = index.query(q)
    return response.response or ""
