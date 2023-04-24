"""GMail` agent example!

It can:
* Check your email and read it for you.
* Search or filter your email.
"""

import base64
import datetime
import json
import sys

import fixieai
import gmail_client

try:
    oauth_params = fixieai.OAuthParams.from_client_secrets_file(
        "gcp-oauth-secrets.json",
        ["https://www.googleapis.com/auth/gmail.readonly"],
    )
except FileNotFoundError:
    print(
        "gcp-oauth-secrets.json was not found! You'll need to generate your own oauth "
        "to deploy this agent. For more info, follow the 4-step instructions here: "
        "https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow#creatingcred"
    )
    sys.exit(4)

USER_TIMEZONE = datetime.timezone(datetime.timedelta(hours=-8))
EMBED_NAME = "doc"

BASE_PROMPT = """I am an intelligent email agent that can check your google mail (Gmail) account for messages.
The messages will end with <END> to indicate the end of the message, \
but I will not print it out in my answer. \
When reading an email, I will print it out faithfully without any changes or making up words.

By default I limit my responses to maximum 10 messages unless instructed otherwise.

search_query can use any of the following operators:
- is:unread/read
- in:inbox/sent/starred/trash/spam
- from:email/name
- to:email/name
- subject:string
- General search (body/title/author/etc): string
- Search for an exact match: " "
"""

FEW_SHOTS = """
Q: What are my latest emails?
Thought: I need to get a list of emails from the user's inbox. \
By default the emails are returned from last to first. \
I will limit the number of emails to 10.
Ask Func[list]: { "limit": 10, "search_query": "in:inbox" }
Func[list] says: https://accounts.google.com/o/oauth2/auth?foo=bar
Thought: I need to pass the auth url to the user.
A: I don't have access to your calendar. Please [authorize](https://accounts.google.com/o/oauth2/auth?foo=bar).

Q: What new emails do I have?
Thought: I need to get a list of unread emails from the user's inbox. \
I will limit the number of emails to 10.
Ask Func[list]: { "limit": 10, "search_query": "is:unread in:inbox" }
Func[list] says: You have 2 unread emails in your inbox:
1. [#doc10] Welcome to Fixie!  From: hello@fixie.ai  To: me@mail.com
2. [#doc12] You wouldn't believe what I just heard about XYZ  From news@journal.io
A: You have 2 unread emails:
1. Welcome to Fixie!
2. You wouldn't believe what ...
Q: read me the email from Fixie.
Thought: I need to retrieve the email from hello@fixie.ai by its ID.
Ask Func[get_message]: #doc10
Func[get_message] says: Title: Welcome to Fixie!
From: hello@fixie.ai
To: me@mail.com
Date: Dec 14, 2020
Hi there! Welcome to Fixie! We are so excited to have you on board. \
We hope you enjoy using Fixie as much as we enjoy building it. <END>
Thought: I need to repeat back this email.
A: Title: Welcome to Fixie!
From: hello@fixie.ai
To: me@mail.com
Date: Dec 14, 2020
Hi there! Welcome to Fixie! We are so excited to have you on board. \
We hope you enjoy using Fixie as much as we enjoy building it.

Q: Get me a list of emails from Jason.
Thought: I need to get a list of emails from Jason.
Ask Func[list]: { "limit": 10, "search_query": "from:Jason in:inbox" }
Func[list] says: You have 3 emails from Jason in your inbox:
1. [#doc8] We Are in Trouble  From: Jason jason_dude@gmail.com  To: Myself me@email.com  Date: Dec 14, 2020
2. [#doc10] An update regarding the CRA strike and filing your taxes  From: Jason jason_dude@gmail.com  Date: Apr 12, 2019
3. [#doc7] What a doozy!  From: Jason not_jason@not_jason.com  Date: March 8, 2019
A: You have 3 emails from Jason in your inbox:
1. We Are in Trouble (From: Jason on Dec 14, 2020)
2. An update regarding the CRA strike and filing your taxes (From Jason on Apr 12, 2019)
3. What a doozy! (From: Not Jason on March 8, 2019)
Q: Read me the first and last email
Thought: I need to retrieve the first and last emails from the list by their IDs.
Ask Func[get_message]: #doc8 #doc7
Func[get_message] says: Title: What a doozy!
From: Jason not_jason@not_jason.com
Date: Jan 1, 2021
I just wanted to acknowledge what a tough time this is for everyone, but I'm confident we can find a solution together.
Let me know if you want to chat! <END>
Title: We Are in Trouble
From: Jason jason_dude@gmail.com
To: Myself me@email.com
Date: Dec 14, 2020
Call me ASAP. <END>
Thought: I need to repeat back both emails.
A: Title: What a doozy!
From: Jason not_jason@not_jason.com
Date: Jan 1, 2021
I just wanted to acknowledge what a tough time this is for everyone, but I'm confident we can find a solution together.
Let me know if you want to chat!
Title: We Are in Trouble
From: Jason jason_dude@gmail.com
To: Myself me@email.com
Date: Dec 14, 2020
Call me ASAP.
"""
agent = fixieai.CodeShotAgent(
    BASE_PROMPT, FEW_SHOTS, conversational=True, oauth_params=oauth_params
)


@agent.register_func
def list(
    query: fixieai.Message, oauth_handler: fixieai.OAuthHandler
) -> fixieai.Message:
    """List emails in user's inbox.

    It allows free-form search queries using Gmail search operators, e.g. from/to/subject.
    """
    user_token = oauth_handler.user_token()
    if user_token is None:
        return oauth_handler.get_authorization_url() or ""

    list_args = json.loads(query.text)
    client = gmail_client.GMailClient(user_token)
    # TODO: type-checking for list_args?
    messages = client.list(**list_args)
    if messages:
        embeds = [
            fixieai.Embed(
                content_type="text/plain",
                uri=content_to_uri(msg.long_str(tz=USER_TIMEZONE)),
            )
            for msg in messages
        ]
        message_lines = [
            f"{i+1}. #{EMBED_NAME}{i} " + msg.short_str(tz=USER_TIMEZONE)
            for i, msg in enumerate(messages)
        ]

        # Note not to add "#" at the start of embeds_dict keys.
        embeds_dict = {f"{EMBED_NAME}{i}": embed for i, embed in enumerate(embeds)}

        message_text = f"You have {len(messages)} unread emails:\n" + "\n".join(
            message_lines
        )
        return fixieai.Message(text=message_text, embeds=embeds_dict)
    else:
        return fixieai.Message(text="No emails matched the filter.")


@agent.register_func
def get_message(query: fixieai.Message) -> str:
    """Get and print a specific message.

    It simply loads the text of embeds from a previous `list` command.
    """
    if not query.embeds:
        return "You need to specify the embed ID of the message you want to read."

    for embed in query.embeds.values():
        if embed.content_type != "text/plain":
            return f"I can only read plain-text emails specified by #{EMBED_NAME}."

    embed_texts = [embed.text for embed in query.embeds.values()]
    return "\n\n".join(embed_texts)


def content_to_uri(content: str) -> str:
    return f"data:base64,{base64.b64encode(content.encode('utf-8')).decode('utf-8')}"
