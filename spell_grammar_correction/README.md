# What is this ?

This is the auxiliary code to my medium article X that explains how to build a serverless API with Amazon Lambda and API Gateway.

# What is included here ?

In this example I included the 4 main files to deploy a Lambda function with serverless.
* `app.py`: Main lambda file. Defines the logic to process a given text string using gingerit
* `Dockerfile`: Main Docker file. Wraps the `app.py` and all required libraries to deploy the service to Lambda
* `requirements.txt`: Fixes the version and libraries needed to run gingerit
* `serverless.yml`: Main serverless file. Defines the required services from AWS needed to build our spell and grammar correction service.