Build an Alexa Hello World Skill in ASK Python SDK (using Classes)
=========================================

This tutorial will walk first-time Alexa skills developers through all the 
required steps involved in creating a skill using this hello world template, 
called ‘hello world’. This post assumes you have some familiarity with 
Python (or a similar programming language) and the Alexa Skills Kit.

<img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/quiz-game/header._TTH_.png" />

Concepts
--------

This simple sample has no external dependencies or session management,
and shows the most basic example of how to create a Lambda function for
handling Alexa Skill requests.

Setup
-----

To run this example skill you need to do two things. The first is to
deploy the example code in lambda, and the second is to configure the
Alexa skill to use Lambda.

[![Get Started](https://camo.githubusercontent.com/db9b9ce26327ad3bac57ec4daf0961a382d75790/68747470733a2f2f6d2e6d656469612d616d617a6f6e2e636f6d2f696d616765732f472f30312f6d6f62696c652d617070732f6465782f616c6578612f616c6578612d736b696c6c732d6b69742f7475746f7269616c732f67656e6572616c2f627574746f6e732f627574746f6e5f6765745f737461727465642e5f5454485f2e706e67)](./instructions/1-voice-user-interface.md)

Skills can be built either by implementing ``AbstractRequestHandler`` classes
or by using skill builder's ``request_handler`` decorator. More information
on this can be checked in the [documentation](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/REQUEST_PROCESSING.html#request-handlers).

This sample skill shows how to implement ``AbstractRequestHandler`` class 
and register the handler classes explicitly in the skill builder object. 
The code for this implementation is under [lambda/py](lambda/py) folder.

For the sample skill using the ``decorators`` approach, check 
[skill-sample-python-helloworld-decorators](https://github.com/alexa/skill-sample-python-helloworld-decorators).

Additional Resources
--------------------

### Community

-  [Amazon Developer Forums](https://forums.developer.amazon.com/spaces/165/index.html) : Join the conversation!
-  [Hackster.io](https://www.hackster.io/amazon-alexa) - See what others are building with Alexa.

### Tutorials & Guides

-  [Voice Design Guide](https://developer.amazon.com/designing-for-voice/) -
   A great resource for learning conversational and voice user interface design.

### Documentation

-  [Official Alexa Skills Kit Python SDK](https://pypi.org/project/ask-sdk/)
-  [Official Alexa Skills Kit Python SDK Docs](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/)
-  [Official Alexa Skills Kit Docs](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)

