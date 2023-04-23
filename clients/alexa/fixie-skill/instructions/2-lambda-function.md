# Build an Alexa Hello World Skill in ASK Python SDK
<img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/quiz-game/header._TTH_.png" />

[![Voice User Interface](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/1-locked._TTH_.png)](./1-voice-user-interface.md)[![Lambda Function](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/2-on._TTH_.png)](./2-lambda-function.md)[![Connect VUI to Code](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/3-off._TTH_.png)](./3-connect-vui-to-code.md)[![Testing](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/4-off._TTH_.png)](./4-testing.md)[![Next steps](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/5-off._TTH_.png)](./5-next-steps.md)

## Setting Up A Lambda Function Using Amazon Web Services

In the [first step of this guide](1-voice-user-interface.md), we built the Voice User Interface (VUI) for our Alexa skill.  On this page, we will be creating a Lambda function using [Amazon Web Services](http://aws.amazon.com).  You can [read more about what a Lambda function is](http://aws.amazon.com/lambda), but for the purposes of this guide, what you need to know is that Lambda is where our code lives.  When a user asks Alexa to use our skill, it is our Lambda function that interprets the appropriate interaction, and provides the conversation back to the user.

1.  **Go to http://aws.amazon.com and sign in to the console.** If you don't already have an account, you will need to create one.  [Check out this quick walkthrough for setting up a new AWS account](https://alexa.design/create-aws-account).

    [![Sign In](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/2-1-sign-in-to-the-console._TTH_.png)](https://console.aws.amazon.com/console/home)

2.  **Choose "Services" at the top of the screen, and type "Lambda" in the search box.**  You can also find it in the list of services.  It is in the "Compute" section.

    [![Lambda](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/2-2-services-lambda._TTH_.png)](https://console.aws.amazon.com/lambda/home)

3.  **Check your AWS region.** Lambda only works with the Alexa Skills Kit in four regions: US East (N. Virginia), EU (Ireland), US West (Oregon) and Asia Pacific (Tokyo).  Make sure you choose the region closest to your customers.

    ![Lambda Regions](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/2-3-check-region._TTH_.png)

4.  **Click the "Create a Lambda function" button.** It should be near the top of your screen.

    ![Create Function](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/2-4-create-a-lambda-function._TTH_.png)

5.  **Click on "Author from scratch".**  We will configure our Lambda function next.
    1. These values will only ever be visible to you, but make sure that you name your function something meaningful. "samplePythonHelloWorld" is sufficient if you don't have another idea for a name.

    2. From the "Runtime" dropdown select the python version your system supports.  This tutorial and sample code works with either Python 2.7 or 3.6. To check the python version, try the following command in a terminal
        ```
        $ python --version
        Python 2.7.10
        ```

    3. **Set up your Lambda function role.**  If you haven't done this before, we have a [detailed walkthrough for setting up your first role for Lambda](https://alexa.design/create-lambda-role).  If you have done this before, you only need to select the **Existing role**.

    4. Click **Create function**.

6.  **Configure your trigger.** There are many different AWS services that can trigger a Lambda function, but for the purposes of this guide, we need to select "Alexa Skills Kit." from the left hand side.

    Once you have selected Alexa Skills Kit, scroll down and find the Skill ID verification section.  Although you will want to paste your skill's ID in the Skill ID field, however for this tutorial, click Disable.  Click the **Add** button in the lower right.  Click the orange **Save** button in the top right corner.

7.  **Finish configuring your function**. Click on your function's name (you'll find it in the middle) and scroll to the bottom of the page, you'll see a Cloud9 code editor.

    We have provided the code for this skill [here](../lambda/py). To properly upload this code to Lambda, you'll need to perform the following:
    
    1. This skill uses the [ASK SDK for Python](https://github.com/alexa/alexa-skills-kit-sdk-for-python) for development. The skill code is provided in the [hello_world.py](../lambda/py/hello_world.py), and the dependencies are mentioned in [requirements.txt](../lambda/py/requirements.txt). Download the contents of the [lambda/py](../lambda/py) folder. 
    2. On your system, navigate to the lambda folder and install the dependencies in a new folder called “skill_env” using the following command:
    
        ```
        pip install -r py/requirements.txt -t skill_env
        ```
        
    3. Copy the contents of the `lambda/py` folder into the `skill_env` folder. 
    
        ```
        cp -r py/* skill_env/
        ```
    
    4. Zip the contents of the `skill_env` folder. Remember to zip the **contents** of the folder and **NOT** the folder itself.
    5. On the AWS Lambda console, change the **code entry type** drop-down to **Upload a .ZIP file**, upload the zip created in the previous step.
    6. Change the handler name to ``hello_world.handler`` and click on **Save**.
    
    *(Optional)* Follow the ASK Python SDK [Getting Started](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/GETTING_STARTED.html#adding-the-ask-sdk-for-python-to-your-project) documentation, to check alternative ways of installing the sdk and deploying to AWS Lambda console.

8. (Optional) Click the **Configure test events** dropdown menu on the top of the page.
  
    1. Select 'Alexa Start Session' from the 'Event Template' dropdown.
    2. Type `LaunchRequest` into the 'Event Name' field.
    3. Click the orange 'Create' button at the bottom of the page
    4. Click the **Test** button at the top of the page.
    5. You should see a light green box with the message: *Execution result: succeeded* at the top of the page.

9. **As a final step, copy the ARN value from the top right corner of the screen.** You will need this value in the next section of this guide.

[![Next Step](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/buttons/button_next_connect_vui_to_code._TTH_.png)](3-connect-vui-to-code.md)
