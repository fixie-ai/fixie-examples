from fixieai import agents
import json

BASE_PROMPT = """I am an agent that can manage a portfolio. I interact in a professional manager, as a financial executive would."""

FEW_SHOTS = """
Q: What's in my portfolio?
Ask Func[read]: -
Func[read] says: [{"META": 200}, {"GOOG": 350}, {"AAPL": 100}, {"MSFT": 250}]
A: Here are the contents of your portfolio:
Company | Shares
--- | ---
Meta | 200
Google | 350
Apple | 100
Microsoft 250

Q: Add 50 shares of Amazon to my portfolio.
Ask Func[update]: [{"AMZN": 50}]
Func[update] says: Done
A: I have added 50 shares of Amazon to your portfolio.

Q: Remove Facebook from my portfolio.
Ask Func[delete]: ["META"]
Func[delete] says: Done
A: I have removed Facebook from your portfolio.

Q: Add the data from this spreadsheet to my portfolio. [other1]
Ask Func[query_embed]: Get the data from this spreadsheet as a JSON object. [other1]
Func[query_embed] says: [{"AMZN": 32}, {"VZ": 16}, {"IBM": 35}]
Ask Func[update]: [{"AMZN": 32}, {"VZ": 16}, {"IBM": 35}]
Func[update] says: Done
A: I have added the data from this spreadsheet to your portfolio.

Q: Export my portfolio in CSV format.
Ask Func[read]: -
Func[read] says: [{"SNAP": 93}, {"META": 22}, {"INTC": 53}]
Thought: I need to convert this to CSV format and put it in a Markdown code block.
A: Here is the CSV data:

```csv
Company,Shares
SNAP,93
META,22
INTC,53
```

Q: How much is my portfolio worth?
Thought: First I need to get the contents of the portfolio.
Ask Func[read]: -
Func[read] says: [{"T": 100}, {"NVDA: 12}, {"C": 80}]
Thought: Now I need to get stock quotes for each stock.
Ask Agent[justin/stock]: Prices for T, NVDA, C
Agent[justin/stock] says: AT&T: $18.43, Nvidia $229.65, Citigroup $48.34
Thought: Now I need to multiply the numbers of shares by the share prices to get the dollar value of each investment.
Thought: Dollar values: AT&T: $18.43 * 100, Nvidia: $229.65 * 12, Citigroup: $48.34 * 80
Thought: Total portfolio value: $1843.00 + $2755.80 + $3867.20 = $8465.00
A: The total value of your portfolio is $8465.00.

Q: Make a pie chart of my portfolio by investment value.
Thought: First I need to get the contents of the portfolio.
Ask Func[read]: -
Func[read] says: [{"T": 100}, {"NVDA: 12}, {"C": 80}]
Thought: Now I need to get stock quotes for each stock.
Ask Agent[justin/stock]: Prices for T, NVDA, C
Agent[justin/stock] says: AT&T: $18.43, Nvidia $229.65, Citigroup $48.34
Thought: Now I need to multiply the numbers of shares by the share prices to get the dollar value of each investment.
Thought: Dollar values: AT&T: $18.43 * 100, Nvidia: $229.65 * 12, Citigroup: $48.34 * 80
Ask Agent[justin/chart]: Make a pie graph for my portfolio based on these dollar values: AT&T: $1843.00, Nvidia $2755.80, Citigroup $3867.20, title it "Portfolio"
Agent[justin/chart] says: Here you go! [image1]
A: Here is a pie chart of your portfolio. [image1]
"""
agent = agents.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def read(query: agents.Message, user_storage: agents.UserStorage) -> str:
    return json.dumps({k: v for (k, v) in user_storage.items()})


@agent.register_func
def update(query: agents.Message, user_storage: agents.UserStorage) -> str:
    text = query.text.replace("[[", "[")
    text = text.replace("]]", "]")
    updates = json.loads(text)
    for update in updates:
        print("update", update)
        for key in update:
            user_storage[key] = update[key]
    return "Done"


@agent.register_func
def delete(query: agents.Message, user_storage: agents.UserStorage) -> str:
    text = query.text.replace("[[", "[")
    text = text.replace("]]", "]")
    deletes = json.loads(text)
    for delete in deletes:
        del user_storage[delete]
    return "Done"
