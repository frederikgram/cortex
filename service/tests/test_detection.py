""" Test the /api/v1/detection/detect endpoint"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_detect():
    """ Test the /api/v1/detection/detect endpoint """

    # Get Absolute Path to Payload
    import os
    payload_path = os.path.join(os.path.dirname(__file__), "test_detect_payload.json")

    # Load Expected Response
    import json
    response_path = os.path.join(os.path.dirname(__file__), "test_detect_response.json")
    expected_response = json.load(open(response_path, "r"))


    # Load Payload
    import json
    payload = json.load(open(payload_path, "r"))        

    # Send Request
    response = client.post("/api/v1/detection/detect", content=json.dumps(payload), headers={"Content-Type": "application/json"})

    # Assert
    assert response.status_code == 200

    # Check Response
    assert response.json() == expected_response