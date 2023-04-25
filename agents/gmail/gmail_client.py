"""A (very) simple client for the Gmail API."""

import base64
import dataclasses
import datetime
import logging
from typing import List, Optional

import bs4
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import credentials as gcreds

logger = logging.getLogger(__name__)

DATE_PRINT_FORMAT: str = "%A %B %d %Y %H:%M"


class GMailClient:
    """A wrapper around GMail API to return clean objects for consumption.

    The API doc can be found here:
        https://developers.google.com/gmail/api/guides
        https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
    """

    def __init__(self, access_token: str):
        self.client = googleapiclient.discovery.build(
            "gmail",
            "v1",
            credentials=gcreds.Credentials(token=access_token),
        )

    def get_message(self, message_id: str, format="full") -> "Message":
        """Get a message by its ID."""
        raw_message = (
            self.client.users()
            .messages()
            .get(
                userId="me",
                format=format,
                id=message_id,
            )
        ).execute()
        return Message.from_raw_message(raw_message)

    def list(
        self,
        search_query: str = "",
        limit: int = 10,
    ) -> List["Message"]:
        """List messages in the inbox.

        The API doc can be found here:
            https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
        """
        query = (
            self.client.users()
            .messages()
            .list(
                userId="me",
                q=search_query,
                maxResults=limit,
            )
        )

        raw_messages = query.execute()
        raw_messages = raw_messages.get("messages", [])

        # TODO: return token for pagination?
        # TODO: parallelize requests?
        return [self.get_message(mini_msg["id"]) for mini_msg in raw_messages]


@dataclasses.dataclass
class Message:
    id: str
    threadId: str
    snippet: Optional[str] = None
    date: Optional[datetime.datetime] = None
    body: Optional[str] = None
    # The following are from payload.headers:
    title: Optional[str] = None
    author: Optional[str] = None
    recipients: Optional[List[str]] = None

    @classmethod
    def from_raw_message(cls, d: dict) -> "Message":
        """Create a Message from a raw message dict."""
        msg = cls(id=d["id"], threadId=d["threadId"], snippet=d.get("snippet", None))

        if "internalDate" in d:
            msg.date = datetime.datetime.fromtimestamp(int(d["internalDate"]) / 1000)

        payload = d.get("payload", None)
        if payload:
            # extract headers
            headers = payload.get("headers", [])
            for header in headers:
                if header["name"] == "Subject":
                    msg.title = header["value"]
                elif header["name"] == "From":
                    msg.author = header["value"]
                elif header["name"] == "To":
                    msg.recipients = header["value"].split(", ")

            # decode body
            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        msg.body = _body_to_human_readable(part["body"]["data"])
            elif "body" in payload and "data" in payload["body"]:
                msg.body = _body_to_human_readable(payload["body"]["data"])
            else:
                logger.warning(f"No body found in message {msg.id}")

        return msg

    def to_str(
        self,
        sep: str = "  ",
        include_body: bool = False,
        include_snippet: bool = False,
        include_recipients: bool = False,
        end: str = " <END>",
        tz: Optional[datetime.timezone] = None,
    ) -> str:
        """Convert the message to a human readable representation."""
        rep = ""
        if self.title:
            rep += f"{self.title}{sep}"
        if self.author:
            rep += f"From: {self.author}{sep}"
        if include_recipients and self.recipients:
            rep += f"To: {', '.join(self.recipients)}{sep}"
        if self.date:
            date = self.date.astimezone(tz) if tz else self.date
            rep += f"Date: {date.strftime(DATE_PRINT_FORMAT)}{sep}"

        if include_snippet and self.snippet:
            rep += f"Snippet: {self.snippet}{sep}"
        if include_body and self.body:
            if sep == "\n":
                # Add extra new-line for readability
                rep += f"{sep}{self.body}{sep}"
            else:
                rep += f"Body: {self.body}{sep}"

        rep = rep.strip() + end

        return rep

    def short_str(self, tz: Optional[datetime.timezone] = None) -> str:
        """A single-line string representation of the message."""
        return self.to_str(sep="  ", tz=tz)

    def long_str(self, tz: Optional[datetime.timezone] = None) -> str:
        """A multi-line string representation of the message."""
        return self.to_str(
            sep="\n",
            include_body=True,
            include_recipients=True,
            tz=tz,
        )


def _body_to_human_readable(body: str) -> str:
    """Convert a base64-encoded body to human-readable text.
    If the body is HTML, we will extract only the text from it.
    """
    body = base64.urlsafe_b64decode(body).decode("utf-8")
    # If the body is HTML, we want to extract the text from it.
    body = bs4.BeautifulSoup(body, "html.parser").get_text(separator="\n")
    return body.strip()
