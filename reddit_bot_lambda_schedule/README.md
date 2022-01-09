Reddit bot service with AWS Lambda and EventBridge 

#### **What is this?**
This is the auxiliary code to my medium article "[Deploy a “RemindMe” Reddit Bot Using AWS Lambda and EventBridge](https://betterprogramming.pub/deploy-a-reddit-bot-using-aws-lambda-and-eventbridge-7df793b979b2)" that explains how to deploy a Reddit bot for free with AWS Lambda and EventBridge

#### **What is included here?**
In this example I included the 4 main files to deploy a Lambda function with serverless.

* `app/app.py`: Main lambda file. Defines the logic to process reminder requests
* `app/requirements.txt`: Fixes the version and libraries needed to run praw
* `Dockerfile`: Main Docker file. Wraps the `app/app.py` and all required libraries to deploy the service to Lambda
* `serverless.yml`: Main serverless file. Defines the required services from AWS needed to build our reddit bot service.