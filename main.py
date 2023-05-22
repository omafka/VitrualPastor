# !/usr/bin/python

# This is an API chatbot with a history for each session
# Maintains a conversation and answers questions in a predefined style
import os
import json

import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from pydantic import BaseModel
from dotenv import load_dotenv
# Import the Secret Manager client library
from google.cloud import secretmanager

load_dotenv()  # take environment variables from .env.


class Question(BaseModel):
    id_session: str
    text: str
    number_template: int


try:
    # create the Secret Manager client
    client = secretmanager.SecretManagerServiceClient()
    # get OpenAI API key
    name = "projects/number_project/secrets/OpenAI-API/versions/latest"

    response = client.access_secret_version(name=name)
    openai.api_key = response.payload.data.decode("UTF-8")
except Exception:
    openai.api_key = os.environ['OPENAI_API_KEY']


# list of templates
with open('config.json') as f:
    templates = json.load(f)

app = FastAPI()

# for CORS policy
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# chat history for each session
user_histories = {}


@app.get("/")
def read_root():
    return {
        "message": "Make a post request to /ask to ask a question by virtual pastor"
    }


@app.post("/ask")
def ask(question: Question):
    # define user history
    if question.id_session not in user_histories:
        user_histories[question.id_session] = ConversationBufferWindowMemory(k=15)

    current_history = user_histories[question.id_session]

    # define template from config
    if 2 < question.number_template < 0:
        raise HTTPException(status_code=400, detail="Invalid number_template")

    system_content = templates['prompt_templates'][question.number_template]['prompt_template']

    template = system_content + """{history}
                Human: {human_input}
                Assistant:"""

    # define prompt with template
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template
    )

    # define model with history
    chatgpt_chain = LLMChain(
        llm=OpenAI(model_name='gpt-3.5-turbo', temperature=0.5),
        prompt=prompt,
        verbose=True,
        memory=current_history,
    )

    # get answer to the questions
    response = chatgpt_chain.predict(human_input=question.text)

    return {
        "response": response,
    }
