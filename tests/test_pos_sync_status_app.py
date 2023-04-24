import os
import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
from main import app
 
# Declaring test client
client = TestClient(app)
 
# # Test for status code for get message
def test_POSSyncStatus_getPOSSyncStatusToptwo():
    response = client.get("/api/POSSyncStatus/getPOSSyncStatusToptwo")
    assert response.status_code == 200
    response = client.put("/api/POSSyncStatus/getPOSSyncStatusToptwo")
    assert response.status_code == 405

def test_POSSyncStatus_get():
    response = client.get("/api/POSSyncStatus/get")
    assert response.status_code == 200
    response = client.put("/api/POSSyncStatus/get")
    assert response.status_code == 405
    response = client.put("/api/POSSyncStatus/gett")
    assert response.status_code == 404
