# lambda supported docker image
FROM public.ecr.aws/lambda/python:3.8 AS builder

# install required packages
COPY app/requirements.txt ./
RUN pip install -r ./requirements.txt

# copy app to docker
COPY app/app.py ./

# this is the image entrypoint
CMD ["app.lambda_handler"]