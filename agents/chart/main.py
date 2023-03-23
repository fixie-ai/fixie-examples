import urllib.parse

import fixieai

BASE_PROMPT = """I am an agent that makes sick charts."""

FEW_SHOTS = """
Q: Make a chart of the 5 tallest mountains
Thought: I need to make a JSON object with information about the 5 tallest mountains.
Ask Func[chart]: {"type":"bar","data":{"labels":["Mount Everest","K2","Kangchenjunga","Lhotse","Makalu"], "datasets":[{"label":"Height (m)","data":[8848,8611,8586,8516,8485]}]}}
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a pie chart showing the population of the world by continent
Thought: I need to make a JSON object with information about the population of the world by continent.
Ask Func[chart]: {"type":"pie","data":{labels:["Africa","Asia","Europe","North America","South America","Oceania"], "datasets":[{"label":"Population (millions)","data": [1235.5,4436.6,738.8,571.4,422.5,41.3]}]}}   
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a line chart showing the average daily temperature in Seattle by month
Thought: I need to make a JSON object with information about the average daily temperature in Seattle by month.
Ask Func[chart]: {"type":"line","data":{"labels":["January","February","March","April","May","June","July","August","September","October","November","December"], "datasets":[{"label":"Average Temperature (°F)","data":[45,47,50,54,60,65,68,67,63,56,48,45]}]}}   
Func[chart] says: #image1
A: Here you go! #image1
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def chart(query: fixieai.Message) -> fixieai.Message:
    url = "https://quickchart.io/chart?c=" + urllib.parse.quote(query.text)
    embed = fixieai.Embed(content_type="image/png", uri=url)
    return fixieai.Message(text="Here you go! #image1", embeds={"image1": embed})
