"""This is a Fixie Agent that files issues in GitHub."""

import os

import fixieai
from github import Github

# Add a GITHUB_ACCESS_TOKEN to the .env file in this directory before deploying the agent.
# The token needs read/write access to the repo you want to file issues against.
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
if not GITHUB_ACCESS_TOKEN:
    raise ValueError("GITHUB_ACCESS_TOKEN is not set!")

gh = Github(GITHUB_ACCESS_TOKEN)
# This example Agent files issues against the Fixie SDK repo. Change the following to use a different
# repo.
REPO = gh.get_repo("fixie-ai/fixie-sdk")
LABEL = REPO.get_label("user-reported")

BASE_PROMPT = """I am an agent that files bug reports to GitHub."""

FEW_SHOTS = """
Q: File a bug
Thought: I need to get the details from the user.
A: Sure! What was the problem?
Q: The stock price agent seems to be broken
Thought: I need to see if the user would like to upload a file.
A: Okay, thanks for letting me know. Would you like to upload a file, such as a screenshot, to include in the bug report?
Q: No
Thought: I need to make sure the user has provided all of the details.
A: Okay. Is there any additional information you would like to add to the report?
Q: the agent was quoting prices in Icelandic Krona instead of US dollars
Thought: I need to file a bug report, and include all of this information.
Ask Func[file_bug]: The stock price agent seems to be broken. The user says that the agent \
was quoting prices in Icelandic Krona instead of US dollars.
Func[file_bug] says: https://github.com/fixie-ai/fixie/issues/1055
Thought: I need to send the URL to the user.
A: All right, I filed a bug report for you. The issue is https://github.com/fixie-ai/fixie/issues/1055. \
Feel free to edit that issue if you would like to add any additional information. Thanks for your feedback!

Q: File an issue
Thought: I need to get the details from the user.
A: Sure! What is the issue?
Q: The console is spewing nonsense error messages.
Thought: I need to see if the user would like to upload a file.
A: Okay, thanks for letting me know. Would you like to upload a file, such as a screenshot, to include in the bug report?
Q: Yes
Thought: I need to prompt the user to upload the file.
A: Great. Please upload the file now and I'll include it in the bug report.
Q: Here you go #1
Thought: I need to make sure the user has provided all of the details.
A: Okay. Is there any additional information you would like to add to the report?
Q: nope
Thought: I need to file a bug report, and include all of this information.
Ask Func[file_bug]: The console is spewing nonsense error messages. #1
Func[file_bug] says: https://github.com/fixie-ai/fixie/issues/1172
Thought: I need to send the URL to the user.
A: All right, I filed a bug report for you. The issue is https://github.com/fixie-ai/fixie/issues/1172. \
Feel free to edit that issue if you would like to add any additional information. Thanks for your feedback!

Q: The weather agent seems to be broken
Thought: This is a bug report. Get more details from the user.
A: Thanks. Could you please tell me more about the issue?
Q: I asked for the weather in New York and it returned the weather in Sao Paolo.
Thought: I need to see if the user would like to upload a file.
A: Okay, thanks for letting me know. Would you like to upload a file, such as a screenshot, to include in the bug report?
Q: Yes
Thought: I need to prompt the user to upload the file.
A: Great. Please upload the file now and I'll include it in the bug report.
Q: screenshot #1
Thought: I need to make sure the user has provided all of the details.
A: Thank you. Is there any additional information you would like to add to the report?
Q: Yes, I'm running this on a Raspberry Pi 4.
Thought: I need to file a bug report, and include all of this information.
Ask Func[file_bug]: The weather agent seems to be broken. The user asked for the weather in \
New York and it returned the weather in Sao Paolo. The user mentioned they were running \
it on a Raspberry Pi 4.
Func[file_bug] says: https://github.com/fixie-ai/fixie/issues/2798
Thought: I need to send the URL to the user.
A: All right, I filed a bug report for you. The issue is https://github.com/fixie-ai/fixie/issues/2798. \
Feel free to edit that issue if you would like to add any additional information. Thanks for your feedback!
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, conversational=True)


@agent.register_func
def file_bug(query: fixieai.Message) -> str:
    """Files a bug with GitHub."""
    print("file_bug called with query", query)
    title = f"🐛 Bug report from user: {query.text}"
    body = (
        f"This is an automated bug report from the `bug-report` agent.\n"
        + f"The bug report message is as follows:\n\n{query.text}\n\n"
    )
    issue = REPO.create_issue(title=title, body=body, labels=[LABEL])
    return issue.html_url or "I couldn't file the bug report."
