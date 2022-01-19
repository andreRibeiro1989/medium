## Develop a Conversational Bot in 4 simple steps

#### **What is this?**
This is the auxiliary code to my medium article "[Develop a Conversational Bot in 4 simple steps](https://towardsdatascience.com/develop-a-conversational-ai-bot-in-4-simple-steps-1b57e98372e2)" that explains how to create a ChatBot using PyTorch transformers, FastAPI and Docker

#### **What is included here?**

* `app/main.py`: Main app file and docker entrypoint. This defines the FastAPI logic;
* `app/model.py`: Utility file that defines the model's logic;
* `app/static/`: Contains the icons and CSS files
* `app/templates/`: Contains the `index.html` template file that will be modified at run time with the dialog HTML using jinja
* `Dockerfile`: Defines the steps needed to install all required libraries, and run the FastAPI app (`app.main.py`).
* `test/test_app.ipynb`: Testing notebook file

#### **How to run?**
1. Clone the repository to your local machine
2. Build the docker container `docker build . -t chatbot`
3. Run the container `docker run -p 8000:8000 chatbot`
4. Type http://0.0.0.0:8000/ in your favorite browser to interact with the app
