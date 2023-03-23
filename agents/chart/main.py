import urllib.parse

import fixieai

BASE_PROMPT = """I am an agent that makes beautiful charts using the Quickchart API."""

FEW_SHOTS = """
Q: Make a chart of the 5 tallest mountains
Thought: I need to ask the router agent for the 5 tallest mountains and their elevations.
Ask Agent[router]: What are the 5 tallest mountains and their elevations?
Agent[router] says: The 5 tallest mountains and their elevations are Mount Everest at 8848m, K2 at 8611m, Kangchenjunga at 8586m, Lhotse at 8516m, and Makalu at 8485m.
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"bar","data":{"labels":["Mount Everest","K2","Kangchenjunga","Lhotse","Makalu"], "datasets":[{"label":"Height (m)","data":[8848,8611,8586,8516,8485]}]}}
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a pie chart showing the population of the world by continent
Thought: I need to ask the router agent the population of the world by continent.
Ask Agent[router]: What is the population of the world, broken down by continent?
Agent[router] says: The population of the world by continent is Africa at 1235.5 million, Asia at 4436.6 million, Europe at 738.8 million, North America at 571.4 million, South America at 422.5 million, and Oceania at 41.3 million.
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"pie","data":{labels:["Africa","Asia","Europe","North America","South America","Oceania"], "datasets":[{"label":"Population (millions)","data": [1235.5,4436.6,738.8,571.4,422.5,41.3]}]}}   
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a bar chart with this data: Apples, 75; Oranges, 50; Pears, 25; Cherries; 100; Bananas, 75.
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"bar","data":{"labels":["Apples","Oranges","Pears","Cherries","Bananas"], "datasets":[{"data":[75,50,25,100,75]}]}}
Func[chart] says: #image1
A: Here you go! #image1

Q: Create a line chart showing the average daily temperature in Seattle by month
Thought: I need to ask the router agent the average daily temperature in Seattle by month.
Ask Agent[router]: What is the average daily temperature in Seattle by month?
Agent[router] says: The average daily temperature in Seattle by month is January at 45°F, February at 47°F, March at 50°F, April at 54°F, May at 60°F, June at 65°F, July at 68°F, August at 67°F, September at 63°F, October at 56°F, November at 48°F, and December at 45°F.
Thought: I need to make a JSON object with this data.
Ask Func[chart]: {"type":"line","data":{"labels":["January","February","March","April","May","June","July","August","September","October","November","December"], "datasets":[{"label":"Average Temperature (°F)","data":[45,47,50,54,60,65,68,67,63,56,48,45]}]}}   
Func[chart] says: #image1
A: Here you go! #image1
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
