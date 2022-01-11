Question and Answering app using transformers, Docker and FastAPI.

#### **What is this?**
This is the auxiliary code to my medium article "[Build a Q&A App with PyTorch](https://towardsdatascience.com/build-a-q-a-app-with-pytorch-cb599480e29)" that explains how to build a QA app using a pre-trained transformer model form HuggingFace, Docker and FastAPI.


#### **What is included here?**
In here I included the 4 main files required to create the QA API.

* `app/main.py`: Main app file and docker entrypoint. This defines the FastAPI logic.
* `app/utils.py`: Utility file that defines the model's logic.
* `download_model.sh`: Defines the model to be download and required steps.
* `Dockerfile`: Defines the steps needed to install all required libraries, download the pre-trained model (`download_model.sh`) and run the FastAPI app (`/app`).
* `test/test_app.ipynb`: Test the app `set_context` and `get_answer` endpoints.

#### **How to run?**
1. Clone the repository to your local machine
2. Build the docker container `docker build . -t qamodel`
3. Run the container `docker run -p 8000:8000 qamodel`
4. POST to `set_context` endpoint a dictionary containing the following 2 fields to set the model context:
  * `questions` (`list` of `str`): List of strings defining the questions to be embedded
  * `answers` (`list` of `str`): Best answer for each question in 'questions'
5. POST to `get_answer` endpoint a dictionary with the following 1 field to retrieve the most similar question and corresponding answer to a given custom question:
  * `questions` (`list` of `str`): List of strings defining the questions to be embedded
