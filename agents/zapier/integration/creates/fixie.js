
const createFixie = (z, bundle) => {

  var client = require('graphql-client')({
    url: 'https://app.fixie.ai/graphql',
    headers: {
      Authorization: 'Bearer ' + bundle.authData.fixieApiKey
    }
  })

  var variables = {
    handle: bundle.inputData.session,
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
  `, variables, function(req, res) {
    if(res.status === 401) {
      throw new Error('Not authorized')
    }
  })
  .then(function(body) {
    const response = body["data"]["sendSessionMessage"]["response"]["text"];
    console.log("MDW: GOT RESPONSE:")
    console.log(response);
    return { response: response };
  })
  .catch(function(err) {
    console.log("MDW: GOT ERROR:")
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
