'use strict';
const should = require('should');

const zapier = require('zapier-platform-core');

const App = require('../index');
const appTester = zapier.createAppTester(App);


describe('authentication', () => {
  // Put your test TEST_API_KEY in a .env file.
  zapier.tools.env.inject();

  it('should authenticate', (done) => {
    const bundle = {
      authData: {
        fixieApiKey: process.env.TEST_API_KEY
      }
    };

    appTester(App.authentication.test, bundle)
      .then((response) => {
        should.exist(response.username);
        done();
      })
      .catch(done);
  });

});
