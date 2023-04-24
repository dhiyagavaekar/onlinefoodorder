import os
import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
from main import app
 
# Declaring test client
client = TestClient(app)
 

def test_DepartmentType_getAll():
    response = client.get("/api/DepartmentType/getAll")
    assert response.status_code == 200
    response = client.put("/api/DepartmentType/getAll")
    assert response.status_code == 405
    response = client.get("/api/DepartmentType/getAlll")
    assert response.status_code == 404


