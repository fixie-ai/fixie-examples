from fixieai import agents
import yfinance

BASE_PROMPT = """I am an agent that can retrieve stock quotes."""

FEW_SHOTS = """
Q: How did Facebook stock do today?
Thought: I need to get a stock quote for META.
Ask Func[quote]: META
Func[quote] says: $122.98 -1.35%
A: The current share price for Facebook is $122.98, down 1.35% today.

Q: Give me the stock prices for Facebook and Netflix.
Thought: I need to get stock quotes for META and NFLX.
Ask Func[quote]: META
Func[quote] says: $12.34 +0.34%
Ask Func[quote]: NFLX
Func[quote] says: $23.45 +1.14%
A: The share price for Facebook is $12.34, and the share price for Netflix is $23.45.

Q: What is the stock price for the company that makes Kindles?
Thought: The user is asking about a stock price for Amazon.
Thought: I need to get a stock quote for AMZN.
Ask Func[quote]: AMZN
Func[quote] says: $122.98 -1.42%
A: The share price for Amazon is $122.98.

Q: Price for NVDA
Ask Func[quote]: NVDA
Func[quote] says: $99.11 +0.43%
A: The share price for NVDA is $99.11.

Q: Apple share price
Thought: I need to get a stock quote for AAPL.
Ask Func[quote]: AAPL
Func[quote] says: $34.52 +0.17%
A: The share price for Apple is $34.52.

Q: What is the current price for Google?
Thought: I need to get a stock quote for GOOG
Ask Func[quote]: GOOG
Func[quote] says: $123.45 -4.11
A: The current price for GOOG is $123.45.
"""
agent = agents.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


def format_cents(amount: str):
  dot = amount.index(".")
  return amount[:dot + 3]


def get_price(symbol: str):
  info = yfinance.Ticker(symbol).fast_info
  change = info.last_price - info.previous_close
  percent_change = change / info.last_price * 100
  price_str = format_cents(str(info.last_price))
  percent_str = format_cents(str(percent_change))
  if percent_str[0] != "-":
    percent_str = "+" + percent_str
  return price_str, percent_str


@agent.register_func
def quote(query: agents.AgentQuery) -> str:
  symbol = query.message.text
  price, change = get_price(symbol)
  return f"${price} {change}%"


agent.serve("stock")
