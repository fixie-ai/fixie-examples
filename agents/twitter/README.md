# Twitter agent

This Agent answers questions about Twitter activity. To use it, need to make the following changes:

1. Get a Twitter API key from: https://developer.twitter.com/en/portal/petition/essential/basic-info

2. Create a `.env` file in this directory, and add the following environment variable:

```
TWITTER_BEARER_TOKEN=<your Twitter bearer token>
```

3. Run `fixie deploy` to deploy the Agent to Fixie. You can start a session with the Agent and ask
it about recent activity on Twittter.
