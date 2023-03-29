'use strict';
const should = require('should');

const zapier = require('zapier-platform-core');

const App = require('../index');
const appTester = zapier.createAppTester(App);

const SESSION_HANDLE = 'nice-violet-zephyr';

describe('fixie', () => {
  // Put your FIXIE_API_KEY in a .env file to run these tests.
  zapier.tools.env.inject();

  it('should send a Fixie message', (done) => {
    const bundle = {
      authData: {
        fixieApiKey: process.env.FIXIE_API_KEY
      },
      inputData: {
        query: '@fixie/calc What is 432 * 75?'
      }
    };
    appTester(App.creates.fixie.operation.perform, bundle)
      .then((response) => {
        done();
      })
      .catch(done);
  });
});
