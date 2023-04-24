import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
from main import app

# Declaring test client
client = TestClient(app)

def test_Item_Price_Group_Delete():
     response = client.delete("api/ItemPriceGroup/delete/16696/13484472")
     assert response.status_code == 200
     response = client.put("api/ItemPriceGroup/delete/16696/13484472")
     assert response.status_code == 405
     response = client.delete("api/ItemPriceGroup/deletewedd/16696/13484472")
     assert response.status_code == 404
     response = client.delete("api/ItemPriceGroup/delete/'sadddc'/13484472")
     assert response.status_code == 500
     