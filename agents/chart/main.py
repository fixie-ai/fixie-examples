import urllib.parse

import fixieai

BASE_PROMPT = """I am an agent that makes beautiful charts using the Quickchart API."""

FEW_SHOTS = """
Q: Make a chart with the following data: 67, 89, 44, 32, 44.3
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"bar","data":{"datasets":[{"data":[67,89,44,32,44.3]}]}}
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a pie chart showing the following data: Africa, 1235.5; Asia, 4436.6; Europe, 738.8; North America, 571.4; South America, 422.5; Oceania, 41.3.
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"pie","data":{labels:["Africa","Asia","Europe","North America","South America","Oceania"], "datasets":[{"label":"Population (millions)","data": [1235.5,4436.6,738.8,571.4,422.5,41.3]}]}}   
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a bar chart with this data: Apples, 75; Oranges, 50; Pears, 25; Cherries; 100; Bananas, 75.
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"bar","data":{"labels":["Apples","Oranges","Pears","Cherries","Bananas"], "datasets":[{"data":[75,50,25,100,75]}]}}
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a line chart showing this data: 45, 47, 50, 54, 60, 65, 68, 67, 63, 56, 48, 45 with the labels January, February, March, April, May, June, July, August, September, October, November, December.
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"line","data":{"labels":["January","February","March","April","May","June","July","August","September","October","November","December"], "datasets":[{"data":[45,47,50,54,60,65,68,67,63,56,48,45]}]}}   
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a bar chart showing the world population by country.
Thought: I need the data for this query, I can't help the user with this.
A: Sorry, I don't know how to get that data.
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def chart(query: fixieai.Message) -> fixieai.Message:
    url = "https://quickchart.io/chart?c=" + urllib.parse.quote(query.text)
    # Embed URLs are currently limited to 1024 characters.
    if len(url) > 1023:
        return fixieai.Message(text="Sorry, that chart is too big for me to make.")
    embed = fixieai.Embed(content_type="image/png", uri=url)
    return fixieai.Message(text="Here you go! #image1", embeds={"image1": embed})
