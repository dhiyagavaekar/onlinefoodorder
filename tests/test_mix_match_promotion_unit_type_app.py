import os
import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
from main import app
 
# Declaring test client
client = TestClient(app)
 
# # Test for status code for get message
def test_MixMatchPromotionUnitType_getAll():
    response = client.get("/api/MixMatchPromotionUnitType/getAll")
    assert response.status_code == 200
    response = client.put("/api/MixMatchPromotionUnitType/getAll")
    assert response.status_code == 405