# Fixie Notion Agent

This is an example Fixie Agent that indexes a list of web pages, the URLs for which are stored in a
Notion database, and answers questions about them.

## Setup

You'll need to create a Notion integration, which you can configure here: https://www.notion.so/my-integrations

Your integration will need to have "Read Content" permissions on Notion.

Once you create your Integration, get the Integration Token from the integration's page on Notion,
and save it to a file called `notion-key.txt` in this directory.

Next, create a Notion database containing a list of URLs. The database should, at minimum,
have a property called `URL`, which should be of the `URL` type.

On the database page on Notion, go to the three dots menu, and click on "Add Connections", and
select your Notion integration. This gives the integration permission to read this database.

Finally, edit the file `main.py` and change the value of the `NOTION_DATABASE_ID` variable to
match the ID of your Notion database. You can find the ID of your database by looking at the URL
in your address bar when you're on the database page. It will look something like this:
```
https://www.notion.so/codexai/b264de3998384f839245bd54faa40d9c?v=a3978a436c334315ab9d3b61a53aaf8a
```
Here, the database ID is `b264de3998384f839245bd54faa40d9c`.

Finally, run `fixie deploy` to deploy the Agent to Fixie. You can start a session with the
Agent and ask it questions about the contents of the web pages in your Notion database.
The first time you run the Agent, it may take a few minutes until the Agent has indexed all
of the pages.