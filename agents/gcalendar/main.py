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
import gcalendar_client
import utils

try:
    oauth_params = fixieai.OAuthParams.from_client_secrets_file(
        "gcp-oauth-secrets.json",
        ["https://www.googleapis.com/auth/calendar.events"],
    )
except FileNotFoundError:
    print(
        "gcp-oauth-secrets.json was not found! You'd need to generate your own oauth "
        "to deploy this agent. For more info, follow the 4 step instructions here: "
        "https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow#creatingcred"
    )
    sys.exit(4)


BASE_PROMPT = """I am intelligent calendar agent that can check your calendar for events \
or suggest available times to meet. I can also create new events. I will summarize \
events by their title and time, unless the user asks for attendees or location."""

FEW_SHOTS = """
Q: What meetings do I have?
Thought: I need to get the events from now onwards.
Func[local_datetime] says: Friday June 24 2022 01:55 PM UTC-08:00
Ask Func[events]: { "start": "June 24 2022 01:55 PM" }
Func[events] says: https://accounts.google.com/o/oauth2/auth?foo=bar
Thought: I need to pass the auth url to the user.
A: I don't have access to your calendar. Please authorize: https://accounts.google.com/o/oauth2/auth?foo=bar

Q: What's on my calendar for today?
Thought: I need to get the events from now to the end of the day.
Func[local_datetime] says: Friday June 24 2022 10:25 AM UTC-08:00
Ask Func[events]: { "start": "June 24 2022 10:25 AM", "end": "June 24 2022 11:59 PM" }
Func[events] says: title: 'Daily sync', start: Friday June 24 2022 10:00:00, \
end: Friday June 24 2022 11:00:00, location: 'Fixie.ai'
title: 'Datadog tutorial', start: Friday June 24 2022 11:00:00, \
end: Friday June 24 2022 11:30:00
Thought: I need to summarize the events.
A: You have a daily sync from 10am to 11am, and a Datadog tutorial from 11am to 11:30am.

Q: What's on my calendar for the next week?
Thought: I need to get the events from next Monday to next Friday.
Ask Agent[time]: Tell me the exact date of next Monday
Agent[time] says: Next Monday is December 12 2022.
Ask Agent[time]: Tell me the exact date of next Friday
Agent[time] says: Next Friday is December 16 2022.
Ask Func[events]: { "start": "December 12 2022 12:01 AM", \
"end": "December 16 2022 11:59 PM" }
Func[events] says: title: 'Daily sync', start: Monday December 12 2022 10:00:00, \
end: Monday December 12 2022 11:00:00, location: 'Fixie.ai'
title: 'Out of Office', start: Monday December 12 2022 00:00:00, \
end: Wednesday December 14 2022 11:00:00
title: 'Daily sync', start: Tuesday December 13 2022 10:00:00, \
end: Tuesday December 13 2022 11:00:00, location: 'Fixie.ai'
title: 'Daily sync', start: Wednesday December 14 2022 10:00:00, \
end: Wednesday December 14 2022 11:00:00, location: 'Fixie.ai'
title: 'Daily sync', start: Thursday December 15 2022 10:00:00, \
end: Thursday December 15 2022 11:00:00, location: 'Fixie.ai'
title: 'Daily sync', start: Friday December 16 2022 10:00:00, \
end: Friday December 16 2022 11:00:00, location: 'Fixie.ai'
Thought: I need to summarize the events.
A: You have a daily sync at 10am to 11am every day next week, and you are \
Out Of Office from Monday to Tuesday.

Q: Do I have any more meetings today?
Thought: I need to get the events from now to the end of the day.
Func[local_datetime] says: Tuesday August 03 2022 12:35 PM UTC-08:00
Ask Func[events]: { "start": "August 03 2022 12:35 PM", \
"end": "August 03 2022 11:59 PM" }
Func[events] says: You don't have anything scheduled.
Thought: I need to tell the user they don't have anything scheduled.
A: You do not have any more meetings today.

Q: What's on my calendar for next Tuesday?
Ask Agent[time]: Tell me the exact date of next Tuesday
Agent[time] says: Next Tuesday is December 13 2023.
Ask Func[events]: { "start": "December 13 2023 12:01 AM", \
"end": "December 13 2023 11:59 PM" }
Func[events] says: title: 'custom meeting', \
start: Tuesday December 13 09:00:00, end: Tuesday December 13 11:00:00
title: 'static meeting', start: Tuesday December 13 10:00:00, \
end: Tuesday December 13 12:30:00, location: 'https://us06web.zoom.us/j/88345451280'
title: 'Daily sync', start: Tuesday December 13 13:00:00, \
end: Tuesday December 13 14:00:00, location: 'Fixie.ai'
Thought: I need to summarize the events.
A: You have a custom meeting from 9am to 11am, a static meeting from 10am to 12:30pm \
and a daily sync from 1pm to 2pm.

Q: When is my workout scheduled for?
Thought: I need to get the events from now onwards, and see if any of them match gym.
Func[local_datetime] says: Tuesday December 13 2022 08:35 AM UTC-08:00
Ask Func[events]: { "start": "December 13 2022 08:35 AM" }
Func[events] says: title: 'Pair programming - build a Notion Agent', \
start: Tuesday December 13 09:00:00, end: Tuesday December 13 10:00:00
title: 'gym', start: Wednesday December 14 17:00:00, \
end: Wednesday December 14 18:00:00
title: 'Standup', start: Thursday December 15 09:00:00, \
end: Thursday December 15 10:00:00
title: 'yoga', start: Thursday December 15 09:00:00, \
end: Thursday December 15 10:00:00
Thought: There's a yoga and a gym event scheduled. I need to report back those.
A: You have a gym scheduled for Wednesday from 5pm to 6pm, and a yoga scheduled \
for Thursday from 9am to 10am.

Q: Do I have time for an hour long meeting tomorrow?
Thought: I need to look for 1 hour of available time in user's work hours tomorrow.
Func[workhours] says: 09:00 AM to 05:00 PM
Ask Agent[time]: What is tomorrow's date?
Agent[time] says: Tomorrow is December 21 2022
Ask Func[availability]: { \
"start": "December 21 2022 09:00 AM", \
"end": "December 21 2022 05:00 PM", \
"duration": "1:00:00" \
}
Func[availability] says: [["Wednesday December 21 2022 10:00", \
"Wednesday December 21 2022 13:00", ]]
Thought: I need to tell the user about their options.
A: You can have an hour long meeting tomorrow at 10am or at 1pm.

Q: Do I have time for a 2 hours long meeting on next week's Wednesday?
Thought: I need to look for 2 hours of available time in user's work hours next week's \
Wednesday.
Func[workhours] says: 10:00 AM to 06:00 PM
Ask Agent[time]: Tell me the exact date of next week's Wednesday.
Agent[time] says: Next week's Wednesday is December 21 2022
Ask Func[availability]: \
{ "start": "December 21 2022 10:00 AM", \
"end": "December 21 2022 06:00 PM", \
"duration": "2:00:00" }
Func[availability] says: [["Wednesday December 21 2022 10:00", \
"Wednesday December 21 2022 13:00" ]]
Thought: I need to tell the user about their options.
A: You can have a 2 hours long meeting next week Wednesday at 10am or 1pm.

Q: Do I have time for an hour long meeting on next week's Tuesday?
Thought: I need to look for 1 hour of available time in user's work hours next Tuesday.
Func[workhours] says: 09:00 AM to 05:00 PM
Ask Agent[time]: Tell me the exact date of next week's Tuesday.
Agent[time] says: Next week's Tuesday is December 20 2022
Ask Func[availability]: \
{ "start": "December 20 2022 09:00 AM", \
"end": "December 20 2022 05:00 PM", \
"duration": "2:00:00" }
Func[availability] says: [["Tuesday December 20 2022 10:00", \
"Tuesday December 20 2022 13:00", "Tuesday December 20 2022 14:00", \
"Tuesday December 20 2022 15:00" ]]
Thought: I need to tell the user about their options.
A: You can have an hour long meeting next week Tuesday at 10am, 1pm, 2pm or 3pm.

Q: Can you schedule an hour-long meeting with developers@fixie.ai on Tuesday at 10am \
to discuss M4 readiness?
Ask Agent[time]: Tell me the exact date of Tuesday.
Agent[time] says: Tuesday is December 27 2022
Thought: I need to schedule a new event.
Ask Func[schedule]: \
{ "start": "December 27 2022 10:00 AM", \
"duration": "1:00:00", \
"title": "M4 Readiness", "attendees": [["developers@fixie.ai"]]}
Func[schedule] says: title: 'the awesome meeting', \
start: Tuesday December 27 2022 10:00, end: Tuesday December 27 2022 11:00 is scheduled
A: I scheduled an hour long meeting 'the awesome meeting' with the team for Tuesday \
at 10am.

Q: Can you schedule a half an hour meeting with developers@fixie.ai ASAP to discuss \
the demo?
Thought: I first need to ask the calendar agent for the first available half an hour \
time slot.
Ask Agent[gcalendar]: When is the first available half an hour time slot for me?
Agent[gcalendar] says: You are free tomorrow from 9am to 10am and then from 2pm to 5pm.
Thought: I'm going to schedule a meeting at 9am tomorrow since it's the first \
available slot.
Ask Agent[time]: What is tomorrow's date?
Agent[time] says: Tomorrow is Tuesday December 27
Ask Func[schedule]: \
{ "start": "Tuesday December 27 09:00 AM", \
"duration": "0:30:00", \
"title": "Discuss the Demo", "attendees": [["developers@fixie.ai"]] }
Func[schedule] says: title: 'Discuss the Demo', \
start: Tuesday December 27 2022 9:00, end: Tuesday December 27 2022 9:30 is scheduled
A: I scheduled a 30 minutes meeting 'Discuss the Demo' with developers@fixie.ai \
for tomorrow at 9am.

Q: Schedule a 45 minutes event titled "the custom meeting title" for Friday
Thought: I first need to ask the calendar agent for the availability on Friday.
Ask Agent[gcalendar]: Do I have time for a 45 minutes meeting on Friday?
Agent[gcalendar] says: You are free from 9am to 10am and then from 2pm to 5pm.
Thought: I'm going to schedule a meeting at 9am since it's the first available slot.
Ask Agent[time]: What is Friday's exact date?
Agent[time] says: Friday is December 23 2022
Ask Func[schedule]: \
{ "start": "December 23 2022 09:00 AM", \
"duration": "0:45:00", \
"title": "the custom meeting title" }
Func[schedule] says: title: 'the custom meeting title', \
start: Friday December 23 2022 9:00, end: Friday December 23 2022 9:45 is scheduled
A: I scheduled a 45 minutes meeting 'the custom meeting title' for tomorrow at 9am.

Q: Schedule a 2 hours long sync meeting next week with somegiven@email.com
Thought: I first need to ask the calendar agent for the availability the next week.
Ask Agent[gcalendar]: Do I have time for a 2 hours long meeting next week?
Agent[gcalendar] says: You have two hours available on Thursday from 1pm to 3pm.
Ask Agent[time]: Tell me the exact date of next Thursday
Agent[time] says: Next Thursday is December 22 2022
Thought: I'm going to schedule a meeting on next Thursday at 1pm.
Ask Func[schedule]: \
{ "start": "December 22 2022 01:00 PM", \
"duration": "2:00:00", "title": "sync meeting", "attendees": [["somegiven@email.com"]] }
Func[schedule] says: title: 'the custom meeting title', \
start: Thursday December 22 2022 13:00, end: Thursday December 22 2022 15:00 is \
scheduled
A: I scheduled a 2 hours long meeting 'sync meeting' for next Thursday at 1pm.

Q: Schedule a 45 minute long meeting titled "the calendar test" sometime on next \
week's Wednesday
Thought: I first need to ask the calendar agent for the availability on next \
Wednesday
Ask Agent[gcalendar]: Do I have time for a 45 minutes long meeting next \
Wednesday?
Agent[gcalendar] says: You have 45 minutes available on next Wednesday at 11am, \
11:45am, 2pm, 2:45pm, and 4pm.
Ask Agent[time]: Tell me the exact date of next Wednesday
Agent[time] says: Next Wednesday is December 21 2022
Thought: I'm going to schedule a meeting on next Wednesday at 11am.
Ask Func[schedule]: \
{ "start": "December 21 2022 11:00 AM", \
"duration": "0:45:00", "title": "the calendar test", \
"attendees": [["somegiven@email.com"]] }
Func[schedule] says: title: 'the calendar test', \
start: Wednesday December 21 2022 11:00, end: Wednesday December 21 2022 11:45 is \
scheduled
A: I scheduled a 45 minutes long meeting 'the calendar test' for next Thursday at \
11am.
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, oauth_params=oauth_params)


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
