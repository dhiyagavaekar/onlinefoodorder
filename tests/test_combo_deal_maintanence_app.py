import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
import requests
import json
from main import app
 
# Declaring test client
client = TestClient(app)
 
# # Test for status code for get message
def test_POSSyncStatus_get():
    response = client.get("api/ComboDealMaintanence/GetComboPriorityTypes")
    assert response.status_code == 200
    response = client.put("api/ComboDealMaintanence/GetComboPriorityTypes")
    assert response.status_code == 405
    response = client.put("api/ComboDealMaintanenceee/GetComboPriorityTypes")
    assert response.status_code == 404




