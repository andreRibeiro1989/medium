Reddit bot service with AWS Lambda and EventBridge 

What is this?
This is the auxiliary code to my medium article X that explains how to deploy a Reddit bot for free with AWS Lambda and EventBridge

What is included here?
In this example I included the 4 main files to deploy a Lambda function with serverless.

* app.py: Main lambda file. Defines the logic to process reminder requests
* Dockerfile: Main Docker file. Wraps the app.py and all required libraries to deploy the service to Lambda
* requirements.txt: Fixes the version and libraries needed to run praw
* serverless.yml: Main serverless file. Defines the required services from AWS needed to build our reddit bot service.