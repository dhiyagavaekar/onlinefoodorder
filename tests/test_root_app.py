"""
Test for the main page using fastapi.testclient.
"""
import os
import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
from main import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Declaring test client
client = TestClient(app)
 
# Test for status code for get message
def test_get_message():
    "asserting status code"
    response = client.get("/")
    assert response.status_code == 200