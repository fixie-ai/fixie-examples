import datetime
from typing import List, Optional

import gcalendar_client

USER_TIMEZONE = datetime.timezone(datetime.timedelta(hours=-8))
USER_DATETIME = datetime.datetime.now(USER_TIMEZONE)
USER_WORK_HOURS = "09:00 AM to 05:00 PM"
DEFAULT_EVENT_DURATION = "0:30:00"


def parse_datetime(s: Optional[str]) -> Optional[datetime.datetime]:
    """Convert an iso formatted datetime string to datetime object in user's timezone."""
    if s is None:
        return None
    d = datetime.datetime.strptime(s, "%B %d %Y %I:%M %p")
    return d.replace(tzinfo=USER_TIMEZONE)


def parse_timedelta(s: Optional[str]) -> datetime.timedelta:
    """Convert an HH:MM:SS timedelta formatted string to a timedelta object."""
    s = s or DEFAULT_EVENT_DURATION
    try:
        parts = s.split(":")
        hours = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 0
        seconds = int(parts[2]) if len(parts) > 2 else 0
    except:
        raise ValueError(f"duration was wrongly formatted: {s}")
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)


def find_available_slots(
    events: List[gcalendar_client.Event],
    start: datetime.datetime,
    end: datetime.datetime,
    duration: datetime.timedelta,
) -> List[datetime.datetime]:
    """Finds a maximal list of possible start times for events of length `duration`
    within [start, end - duration], such that they don't conflict with events in
    `events`.

    Args:
        events: A list of already booked events that the new event should not conflict
            with.
        start: The minimum start datetime for the booked event.
        end: The maximum end datetime for the booked event.
        duration: The length of the event to find availabilities for.
    Returns:
        A maximal list of possible start datetimes.
    """
    # First, sort events by their start time.
    events = sorted(events, key=lambda e: e.start)
    possible_starts: List[datetime.datetime] = []
    # Iterate over the events, and as long as we can fit an event of length duration in
    # [start, event.start] add start as a possible start datetime.
    for event in events:
        while (event.start - start) >= duration:
            possible_starts.append(start)
            start += duration
        start = max(start, event.end)
    # Keep pushing start to the end with steps of length duration and add all as a
    # possible start time.
    while start + duration <= end:
        possible_starts.append(start)
        start += duration
    return possible_starts
