# Datadog Agent

This is a sample Fixie Agent that uses the Datadog API to query logs stored in Datadog.

To use it, create a `.env` file in this directory containing the following:
```
DD_API_KEY=<your Datadog API key>
DD_APP_KEY=<your Datadog app key>
```
The API key is organization-wide, and the App key is specific to your user account.

You can then deploy the Agent with `fixie agent deploy`.