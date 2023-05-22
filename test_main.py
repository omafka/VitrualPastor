# !/usr/bin/python

# Unit tests for FastAPI
# check work get and post requests

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Make a post request to /ask to ask a question by virtual pastor"}


# test if the response is successful
def test_ask():
    response = client.post(
        "/ask",
        json={"id_session": "id0987654321",
              "text": "I want to get to know bible more. What should I do?",
              "number_template": "1"},
    )
    assert response.status_code == 200
    assert "response" in response.json()


# test if an invalid number_template returns an error
def test_ask_bad_number_template():
    # make a request with an invalid number_template
    response = client.post(
        "/ask",
        json={"id_session": "test_session",
              "text": "Hello",
              "number_template": 100}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid number_template"}

