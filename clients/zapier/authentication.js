'use strict';

const authentication = {
  type: 'custom',
  connectionLabel: '{{username}}',
  test: {
    url: 'https://app.fixie.ai/api/user',
  },
  fields: [
    {
      key: 'fixieApiKey',
      type: 'string',
      required: true,
      helpText: 'Find your Fixie API key on your [Fixie Profile page](https://app.fixie.ai/profile).'
    },
  ],
};

module.exports = authentication;

