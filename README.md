# API Chatbot
This is an API chatbot with a history for each session. Maintains a conversation and answers questions in a predefined style. 

## Requirements

It requires Python 3.10, OpenAI (model 'gpt-3.5-turbo'), langchain, and FastAPI.

The OpenAI API key must be in the file '.env' (in format OPENAI_API_KEY=sk..).

## Getting started

1. Install libraries from requirements.txt: ```pip install -r requirements.txt```
2. Bot launch: ```uvicorn main:app --reload```

## Parameters API

### Request body:
- id_session: id session for history

- text: question from a user

- number_template: 
  + 0 - no context
  + 1 - a virtual pastor
  + 2 - Pastor Charles Stanley
