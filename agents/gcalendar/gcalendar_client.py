"""A clean API Google Calendar client."""

import dataclasses
import datetime
from typing import List, Optional

import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import credentials as gcreds

DATE_PRINT_FORMAT: str = "%A %B %d %Y %H:%M"


class GcalendarClient:
    """A wrapper around Google Calendar API to return clean objects for consumption.

    The API doc can be found here:
        https://developers.google.com/calendar/api/v3/reference/events
    """

    def __init__(self, access_token: str):
        self.client = googleapiclient.discovery.build(
            "calendar",
            "v3",
            credentials=gcreds.Credentials(token=access_token),
            static_discovery=False,
        )

    def events(
        self,
        start: Optional[datetime.datetime] = datetime.datetime.utcnow(),
        end: Optional[datetime.datetime] = None,
    ) -> List["Event"]:
        query = self.client.events().list(
            calendarId="primary",
            orderBy="startTime",
            singleEvents=True,  # Repeat recurring events in the results.
            timeMin=_to_utc_iso(start),
            timeMax=_to_utc_iso(end),
            maxResults=20,
        )
        raw_events = query.execute()
        raw_events = raw_events.get("items", [])
        return [Event.from_raw_event(raw_event) for raw_event in raw_events]

    def create_event(
        self,
        title: str,
        description: str,
        attendees: List[str],
        start: datetime.datetime,
        duration: datetime.timedelta = datetime.timedelta(seconds=3600),
    ) -> "Event":
        event = {
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": (start + duration).isoformat()},
            "attendees": [{"email": attendee} for attendee in attendees],
            "summary": title,
            "description": description,
        }
        event = self.client.events().insert(calendarId="primary", body=event).execute()
        return Event.from_raw_event(event)


@dataclasses.dataclass
class Event:
    start: datetime.datetime
    end: datetime.datetime
    title: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    attendees: Optional[List[str]] = None

    @classmethod
    def from_raw_event(cls, d: dict) -> "Event":
        ret = cls(
            start=_datetime(d["start"]),
            end=_datetime(d["end"]),
        )
        ret.title = d.get("summary")
        ret.description = d.get("description")
        ret.creator = _name(d.get("creator")) or _name(d.get("organizer"))
        ret.status = d.get("status")
        ret.location = d.get("location")
        ret.attendees = list(
            filter(None, [_name(attendee) for attendee in d.get("attendees", [])])
        )
        return ret

    def show_in(self, timezone: Optional[datetime.timezone] = None) -> str:
        """Prints the event in a given timezone."""
        info = []
        if self.title is not None:
            info.append(f"title: {self.title!r}")
        if self.start is not None:
            info.append(f"start: {to_localtime_str(self.start, timezone)}")
        if self.end is not None:
            info.append(f"end: {to_localtime_str(self.end, timezone)}")
        if self.location is not None:
            info.append(f"location: {self.location!r}")
        return ", ".join(info)


def to_localtime_str(dt: datetime.datetime, tz: Optional[datetime.timezone] = None):
    """Returns a pretty string to represent the datetime in a given timezone."""
    if tz is not None:
        dt = dt.astimezone(tz)
    return dt.strftime(DATE_PRINT_FORMAT)


def _datetime(d: dict) -> datetime.datetime:
    """Parses a Google Calendar API time dict into a datetime object.

    The result includes the timezone, and so can be converted to any other timezone.
    """
    if "dateTime" in d:
        return datetime.datetime.strptime(d["dateTime"], "%Y-%m-%dT%H:%M:%S%z")
    elif "date" in d:
        return datetime.datetime.strptime(d["date"], "%Y-%m-%d")
    else:
        raise RuntimeError(f"Unknown datetime format from api: {d!r}")


def _name(d: Optional[dict]) -> Optional[str]:
    """Parses a Google Calendar API creator dict into a string creator."""
    if d is None or d.get("resource"):
        return None
    if d.get("self"):
        return "myself"
    else:
        return d.get("displayName") or d.get("email")


def _to_utc_iso(d: Optional[datetime.datetime]) -> Optional[str]:
    if d is None:
        return None
    in_utc = d.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return in_utc.isoformat() + "Z"  # 'Z' indicates UTC
