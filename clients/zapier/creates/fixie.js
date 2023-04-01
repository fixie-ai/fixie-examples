// This is the Zapier integration "create" for Fixie, which creates a new Fixie
// message and returns the response. It uses the graphql-client library to
// interact with the Fixie API.

// Create a new Fixie session.
async function createSession(client) {
  const handle = await client.query(`
    mutation CreateSession {
      createSession {
        session {
          handle
        }
      }
    }
  `, {}, function (req, res) {
    if (res.status === 401) {
      throw new Error('Not authorized')
    }
  }).then(function (body) {
    h = body["data"]["createSession"]["session"]["handle"];
    console.log(`Got handle: ${h}`);
    return h;
  }).catch(function (err) {
    console.log("Got error creating session:");
    console.log(err.message)
    return { error: err.message };
  });
  return handle;
};

// This is the main Fixie create message action.
async function createFixie(z, bundle) {
  var client = require('graphql-client')({
    url: 'https://app.fixie.ai/graphql',
    headers: {
      Authorization: 'Bearer ' + bundle.authData.fixieApiKey
    }
  })

  var handle = bundle.inputData.session;

  if (!handle) {
    // Create a new session.
    handle = await createSession(client);
  }
  console.log(`Sending message to session ${handle}`);

  var variables = {
    handle: handle,
    text: bundle.inputData.query,
  }

  return client.query(`
  mutation SendMessage($handle: String!, $text: String!) {
    sendSessionMessage(messageData: {session: $handle, text: $text}) {
      response {
        text
      }
    }
  }
  `, variables, function (req, res) {
    if (res.status === 401) {
      throw new Error('Not authorized')
    }
  })
    .then(function (body) {
      const response = body["data"]["sendSessionMessage"]["response"]["text"];
      console.log("Got response:");
      console.log(response);
      return { response: response };
    })
    .catch(function (err) {
      console.log("Got error sending message:");
      console.log(err.message)
      return { error: err.message };
    })
};

module.exports = {
  key: 'fixie',
  noun: 'Fixie',

  display: {
    label: 'Send Fixie Message',
    description: 'Sends a message to Fixie.'
  },

  operation: {
    inputFields: [
      { key: 'session', label: 'Session', required: false },
      { key: 'query', label: 'Body', required: true },
    ],
    perform: createFixie
  }
};
