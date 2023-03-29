# Fixie Zapier integration

This is an example of how to integrate Fixie with Zapier.

The `integration` directory contains a Zapier integration that,
when pushed to Zapier, allows you to build Zaps that send messages
to Fixie. As an example, you can configure your Zap to send a message
to Fixie any time there's a new email received, when a Slack message
is sent to a given channel ... anything that Zapier knows how to do.

This is quite bare bones for now, but if you would like to test it out,
here's what you need to do.

1. Install the Zapier CLI:
```
$ npm install -g zapier-platform-cli
```

2. Login to your Zapier account:
```
$ zapier login
```

3. Deploy the Zapier integration:
```
$ cd integration
$ zapier register "Fixie Example Integration"
$ zapier push
```

4. Invite yourself (or others) to use the new Zapier integration:
```
$ zapier users:add youremail@yourdomain.com 1.0.0
```
You will need to accept the invitation from the email that Zapier
sends you to use the integration. When you do so, Zapier will prompt
you to enter your Fixie API token. This can be found on your Fixie user
profile page at https://app.fixie.ai/profile.

5. On the Zapier web UI, create a new Zap and select the "Fixie
Example Integration" app. You should see an action called "Send
Fixie Message".  Select it and fill out the fields. The "Session"
field is the handle of the Session ID that you want to send messages
to. If this is unspecified, a new Session will be created each time
the Zap is triggered. The "Body" field is the text of the query you
want to send to Fixie.

The response from Fixie is returned from the Fixie action and can be
passed along to the next step in your Zap.

## Local development and testing

If you want to test the Zapier integration locally, you need to create
a `.env` file in the `integration` directory. This file should contain
the line `FIXIE_API_KEY` with your Fixie API key:
```
FIXIE_API_KEY=your_fixie_api_key
```

You can then test the Zapier integration using:
```
zapier test
```
