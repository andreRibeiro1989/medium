# lambda supported docker image
FROM public.ecr.aws/lambda/python:3.8 AS builder

# install required packages
COPY requirements.txt ./
RUN pip install -r ./requirements.txt

# copy app to docker
COPY app.py ./

# defines the function in app.py that lambda will use
CMD ["app.lambda_handler"]