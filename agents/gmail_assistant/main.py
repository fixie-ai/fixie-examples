"""Google Calendar agent example!

It can:
* Check your calendar for events.
* Find empty spots in your calendar.
* Schedule new meetings in your calendar.
"""


import datetime
import json
import sys

import fixieai
import gmail_assistant_client
import utils

try:
    oauth_params = fixieai.OAuthParams.from_client_secrets_file(
        "gcp-oauth-secrets.json",
        ["https://www.googleapis.com/auth/calendar.events"],
    )
except FileNotFoundError:
    print(
        "gcp-oauth-secrets.json was not found! You'll need to generate your own oauth "
        "to deploy this agent. For more info, follow the 4-step instructions here: "
        "https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow#creatingcred"
    )
    sys.exit(4)


BASE_PROMPT = """I am intelligent gmail assistant agent that can check your emails \
and generate responses to those emails. \ 
events by their title and time, unless the user asks for attendees or location."""


def getFewShots():
    import os
    folder_path = "C:/fixie/fixie-hack23/agents/trainingdata" # replace with the path to your folder containing text files
    files = os.listdir(folder_path)

    RecievedEmailsdata = {}
    SentEmailsdata = {}

    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r") as f:
                content = f.read()
                key = os.path.splitext(file)[0] # get the filename without the extension
                if "Recieved" in key:
                    RecievedEmailsdata[key] = content
                elif "Sent" in key:
                    SentEmailsdata[key] = content

    fewShots = ""

    for key, value in RecievedEmailsdata:
        responseKey = key.replace(".txt", "")

        responseKey =  responseKey+"response.txt"

        fewShots.add("Q: Answer the email " + value +  "[FUNCS]" + "A: " +
            SentEmailsdata)
        
    return fewShots                          

FEW_SHOTS = """
Q: Answer this email from today? "hi dan how is your day"
Thought: I need to write a response to this email.
Func[answeremail] says: great thanks how is yours"
A: great thanks how is yours

Q: Answer the emails I have got today
Thought: I need to get to the emails from gmail and then write draft responses
Func[dummyemails] says: [{"subject": Urgent Cash Flow Situation,
"time": 13:10 11/03/2023,
"sender": urgentinvestor@gmail.com,
body:Dear Matt,

I regret to inform you that we are experiencing a significant cash flow problem, and we may not be able to meet our payroll obligations this week. We urgently need your assistance in finding a solution to this issue.

Regards,
Investor
}]
Func[respond_emails] says : [{"subject": Urgent Cash Flow Situation,
"time": 13:10 11/03/2023,
"sender": urgentinvestor@gmail.com,
"body":Dear Investor,
Thank you for bringing this urgent cash flow situation to my attention. I understand the gravity of the situation and will work with our finance team to find a solution as soon as possible.

Best,
Matt}]
A: Here is your draft {"subject": Urgent Cash Flow Situation,
"time": 13:10 11/03/2023,
"sender": urgentinvestor@gmail.com,
"body":Dear Investor,
Thank you for bringing this urgent cash flow situation to my attention. I understand the gravity of the situation and will work with our finance team to find a solution as soon as possible.

Best,
Matt}
"""

agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, oauth_params=oauth_params)

def answeremail(query: fixieai.Message):
    print("this got called")
    

@agent.register_func
def workhours():
    """Returns valid working hours. Currently simple."""
    return "09:00 AM to 05:00 PM"


@agent.register_func
def events(query: fixieai.Message, oauth_handler: fixieai.OAuthHandler) -> str:
    """Returns all events in user's calendar for a range.

    query should be in the format:
        {
            "start": "Weekday Month DD YYYY HH:MM",  # default = now
            "end": "Weekday Month DD YYYY HH:MM",    # default = eternity
        }
    """
    user_token = oauth_handler.user_token()
    if user_token is None:
        return oauth_handler.get_authorization_url()

    client = gcalendar_client.GcalendarClient(user_token)
    range_json = query.text
    range_dict = json.loads(range_json)
    start = utils.parse_datetime(range_dict.get("start")) or datetime.datetime.utcnow()
    end = utils.parse_datetime(range_dict.get("end"))
    events = client.events(start=start, end=end)
    if events:
        return "\n".join(f"{event.show_in(utils.USER_TIMEZONE)}" for event in events)
    else:
        return "You don't have anything scheduled."


@agent.register_func
def availability(query: fixieai.Message, oauth_handler: fixieai.OAuthHandler) -> str:
    """Returns a list of possible start datetimes for an event of custom length.

    query should be in the format:
        {
            "start": "Weekday Month DD YYYY HH:MM",  # default = now
            "end": "Weekday Month DD YYYY HH:MM",    # default = now + 1 day
            "duration": "HH:MM:SS"                   # default = 30 min
        }
    """
    user_token = oauth_handler.user_token()
    if user_token is None:
        return oauth_handler.get_authorization_url()

    client = gcalendar_client.GcalendarClient(user_token)
    query_json = json.loads(query.message.just_str())
    start = utils.parse_datetime(query_json.get("start")) or datetime.datetime.utcnow()
    end = utils.parse_datetime(query_json.get("end")) or (
        start + datetime.timedelta(days=1)
    )
    duration = utils.parse_timedelta(query_json.get("duration"))

    # List all events in the asked [start, end] range and find available slots.
    booked_events = client.events(start=start, end=end)
    possible_starts = utils.find_available_slots(booked_events, start, end, duration)

    # Report back the options.
    if possible_starts:
        return str(
            [
                gcalendar_client.to_localtime_str(possible_start, utils.USER_TIMEZONE)
                for possible_start in possible_starts
            ]
        )
    else:
        return "There's no availability on the selected dates for the given duration."


@agent.register_func
def schedule(query: fixieai.Message, oauth_handler: fixieai.OAuthHandler) -> str:
    """Schedules a new meeting at a given time with custom title.

    query should be in the format:
        {
            "start": "Weekday Month DD YYYY HH:MM",  # default = now
            "duration": "HH:MM:SS",                  # default = 30 min
            "title": "Title",                        # default = Untitled
            "attendees": ["john@smith.com", ...],    # default = []
            "description": "Description"             # default = ""
        }
    """
    user_token = oauth_handler.user_token()
    if user_token is None:
        return oauth_handler.get_authorization_url()

    client = gcalendar_client.GcalendarClient(user_token)
    range_json = query.message.just_str()
    range_dict = json.loads(range_json)
    start = utils.parse_datetime(range_dict.get("start")) or datetime.datetime.utcnow()
    duration = utils.parse_timedelta(range_dict.get("duration"))

    title = range_dict.get("title") or "Untitled"
    attendees = range_dict.get("attendees") or []
    description = range_dict.get("description") or ""
    event = client.create_event(
        start=start,
        duration=duration,
        title=title,
        attendees=attendees,
        description=description,
    )
    return f"{event.show_in(utils.USER_TIMEZONE)} is scheduled."
