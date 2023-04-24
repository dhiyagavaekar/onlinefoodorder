import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
import requests
import json
from main import app
import random
# Declaring test client
client = TestClient(app)
 
# # Test for status code for get message
def test_Department_getAll():
    response = client.get("/api/Department/getAll/gk/17")
    assert response.status_code == 200
    response = client.put("/api/Department/getAll/gk/17")
    assert response.status_code == 405
    response = client.get("/api/Department/getAlll/gk/17")
    assert response.status_code == 404
    response = client.get("/api/Department/getAll/gk/QW17")
    assert response.status_code == 500


def test_Department():
    response = client.put(
        "/api/Department/",
        headers = {"Content-Type": "application/json"}, 
        json = {
            "departmentID": 26706,
            "companyID": 17,
            "departmentDescription": "asas"+str(random.randint(111111, 999999)),
            "departmentTypeName": "General",
            "displayPromptMethodID":None,
            "audibleAgeVerificationAlertFlag":False,
            "lastModifiedBy":"gk",
            "activeFlag": True,
            "isDepartmentOpen": False,
            "departmentProfitMargin": 0,
            "profitPercent": 25,
            "minimumOpenSaleAmount": 0,
            "maximumOpenSaleAmount": 0,
            "isModified":False,
            "isFractionalQtyAllowedFlag": False,
            "createdDateTime":"2022-02-02 13:18:27.610",
            "isLoyaltyRedeemEligibleFlag": False,
            "lastModifiedDateTime":"2022-02-02 13:18:27.610",
            "isItemReturnableFlag": True,
            "allowFoodStampsFlag": True,
            "areSpecialDiscountsAllowedFlag": False,
            "salesRestrictionRequiredFlag": True,
            "isDepartmentNegative": False,
            "departmentTypeID": 1,
            "priceRequiredFlag": True,
            "chartOfAccountTypeID": "",
            "chartOfAccountTypeName": ""
        }
        )
    assert response.status_code == 200
    response = client.post(
        "/api/Department/",
        headers = {"Content-Type": "application/json"}, 
        json = {
            "departmentID": 26706,
            "companyID": 17,
            "departmentDescription": "sass"+str(random.randint(111111, 999999)),
            "departmentTypeName": "General",
            "displayPromptMethodID":None,
            "audibleAgeVerificationAlertFlag":False,
            "lastModifiedBy":"gk",
            "activeFlag": True,
            "isDepartmentOpen": False,
            "departmentProfitMargin": 0,
            "profitPercent": 25,
            "minimumOpenSaleAmount": 0,
            "maximumOpenSaleAmount": 0,
            "isModified":False,
            "isFractionalQtyAllowedFlag": False,
            "createdDateTime":"2022-02-02 13:18:27.610",
            "isLoyaltyRedeemEligibleFlag": False,
            "lastModifiedDateTime":"2022-02-02 13:18:27.610",
            "isItemReturnableFlag": True,
            "allowFoodStampsFlag": True,
            "areSpecialDiscountsAllowedFlag": False,
            "salesRestrictionRequiredFlag": True,
            "isDepartmentNegative": False,
            "departmentTypeID": 1,
            "priceRequiredFlag": True,
            "chartOfAccountTypeID": "",
            "chartOfAccountTypeName": ""
        }
        )
    assert response.status_code == 405
    response = client.put(
        "/api/Department/",
        headers = {"Content-Type": "application/json"}, 
        json = {
            "departmentID": "26706",
            "companyID": 17,
            "departmentDescription": "saasass"+str(random.randint(111111, 999999)),
            "departmentTypeName": "General",
            "displayPromptMethodID":None,
            "audibleAgeVerificationAlertFlag":False,
            "lastModifiedBy":"gk",
            "activeFlag": True,
            "isDepartmentOpen": False,
            "departmentProfitMargin": 0,
            "profitPercent": 25,
            "minimumOpenSaleAmount": 0,
            "maximumOpenSaleAmount": 0,
            "isModified":False,
            "isFractionalQtyAllowedFlag": False,
            "createdDateTime":"2022-02-02 13:18:27.610",
            "isLoyaltyRedeemEligibleFlag": False,
            "lastModifiedDateTime":"2022-02-02 13:18:27.610",
            "isItemReturnableFlag": True,
            "allowFoodStampsFlag": True,
            "areSpecialDiscountsAllowedFlag": False,
            "salesRestrictionRequiredFlag": True,
            "isDepartmentNegative": False,
            "departmentTypeID": "",
            "priceRequiredFlag": "",
            "chartOfAccountTypeID": "",
            "chartOfAccountTypeName": ""
        }
        )
    assert response.status_code == 422
    


