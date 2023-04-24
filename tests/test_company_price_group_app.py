import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
from main import app

# Declaring test client
client = TestClient(app)

# # Test for status code for get message

def test_Company_Price_Group_get_By_CompanyID():
   response = client.get("/api/CompanyPriceGroup/getByCompanyID/17")
   assert response.status_code == 200
   response = client.put("/api/CompanyPriceGroup/getByCompanyID/17")
   assert response.status_code == 405
   response = client.get("/api/CompanyPriceGroup/getByCompanyIDDDS/17")
   assert response.status_code == 404
   response = client.get("/api/CompanyPriceGroup/getByCompanyID/xcrs")
   assert response.status_code == 500

def test_Check_Price_Group_Name_By_CompanyID():
   response = client.get("/api/CompanyPriceGroup/CheckPriceGroupNameByCompanyID/CAMEL CORE/570")
   assert response.status_code == 200
   response = client.put("/api/CompanyPriceGroup/CheckPriceGroupNameByCompanyID/CAMEL CORE/570")
   assert response.status_code == 405
   response = client.get("/api/CompanyPriceGroup/CheckPriceGroupNameByCompanyIDDDS/CAMEL CORE/570")
   assert response.status_code == 404
   response = client.get("/api/CompanyPriceGroup/CheckPriceGroupNameByCompanyID/CAMEL 324432CORE/570addas")
   assert response.status_code == 500

def test_Company_Price_Group_Update():
   response = client.put("/api/CompanyPriceGroup/update",
                          headers = {"Content-Type": "application/json"},
                          json = {"companyPriceGroupID": 1002,"companyID": 17,"companyPriceGroupName": "delta","masterPriceGroupID": 123,"groupIDs": "dad","isSuperGroup": True}
                         )
   assert response.status_code == 200
   response = client.put("/api/CompanyPriceGroup/update",
                          headers = {"Content-Type": "application/json"},
                          json = {"companyPriceGroupID": "0dsdfsef","companyID": "apscs","companyPriceGroupName": "delta","masterPriceGroupID": 123,"groupIDs": "testscase","isSuperGroup": True}
                         )
   assert response.status_code == 422
   response = client.post("/api/CompanyPriceGroup/update",
                          headers = {"Content-Type": "application/json"},
                          json = {"companyPriceGroupID": 1002,"companyID": 0,"companyPriceGroupName": "string","masterPriceGroupID": "string","groupIDs": "string","isSuperGroup": True}
                         )
   assert response.status_code == 405

   response = client.put("/api/CompanyPriceGroup/update",
                          headers = {"Content-Type": "application/json"},
                          json = {"companyPriceGroupID": 1002,"companyID": 17,"companyPriceGroupName": "delta","masterPriceGroupID": "asw","groupIDs": "dad","isSuperGroup": True}
                         )
   assert response.status_code == 500

def test_Company_Price_GroupID_By_CompanyID_delete():
   response = client.delete("/api/CompanyPriceGroup?id=666")
   assert response.status_code == 200
   response = client.delete("/api/CompanyPriceGroup?id=dsadasce")
   assert response.status_code == 500
   response = client.put("/api/CompanyPriceGroup?id=dsadadss")
   assert response.status_code == 405