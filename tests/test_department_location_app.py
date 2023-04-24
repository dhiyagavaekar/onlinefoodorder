import os
import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
from main import app
import random

# Declaring test client
client = TestClient(app)
 
def test_DepartmentLocation_getByDepartmentId():
    response = client.get("/api/DepartmentLocation/getByDepartmentId/23128/gk/763")
    assert response.status_code == 200
    response = client.put("/api/DepartmentLocation/getByDepartmentId/23128/gk/763")
    assert response.status_code == 405
    response = client.get("/api/DepartmentLocation/getByDepartmentId/23128/gk/763/123")
    assert response.status_code == 404
    response = client.get("/api/DepartmentLocation/getByDepartmentId/2312qwe8/gk12/76as3")
    assert response.status_code == 500


def test_DepartmentLocation_post():
    response = client.post(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
        "storeLocationID": 38,
        "departmentID": 1022,
        "posDepartmentCode": "abc"+str(random.randint(111111, 999999)),
        "posSyncStatusID": 0,
        "storeLocationTaxID": 0,
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "abc"+str(random.randint(111111, 999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 201
    response = client.post(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
        "storeLocationID": 38,
        "departmentID": 1022,
        "posDepartmentCode": "abdasdasdasddsadc"+str(random.randint(1111111, 9999999)),
        "posSyncStatusID": 0,
        "storeLocationTaxID": 0,
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "aasdasdasdasdsadasdabc"+str(random.randint(1111111, 9999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 500
    response = client.post(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
        "storeLocationID": "38",
        "departmentID": "1022",
        "posDepartmentCode": random.randint(111111, 999999),
        "posSyncStatusID": "0",
        "storeLocationTaxID": "asc",
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "abc"+str(random.randint(111111, 999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 422
    response = client.post(
        "/api/DepartmentLocations",
        headers = {"Content-Type": "application/json"}, 
        json={
        "storeLocationID": 38,
        "departmentID": 1022,
        "posDepartmentCode": "abc"+str(random.randint(111111, 999999)),
        "posSyncStatusID": 0,
        "storeLocationTaxID": 0,
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "abc"+str(random.randint(111111, 999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 404
    
    
def test_DepartmentLocation_put():
    response = client.put(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
        'departmentLocationID':11150675,
        "storeLocationID": 38,
        "departmentID": 1022,
        "posDepartmentCode": "abc"+str(random.randint(111111, 999999)),
        "posSyncStatusID": 0,
        "storeLocationTaxID": 0,
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "abc"+str(random.randint(111111, 999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 200
    response = client.put(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
        'departmentLocationID':11150675,
        "storeLocationID": 38777777777771298839129372198379127391279,
        "departmentID": 1022,
        "posDepartmentCode": "abdasdasdasddsadc"+str(random.randint(1111111, 9999999)),
        "posSyncStatusID": 0,
        "storeLocationTaxID": 0,
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "aasdasdasdasdsadasdabc"+str(random.randint(1111111, 9999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 500
    response = client.put(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
        'departmentLocationID':11150675,
        "storeLocationID": "38",
        "departmentID": "1022",
        "posDepartmentCode": random.randint(111111, 999999),
        "posSyncStatusID": "0",
        "storeLocationTaxID": "asc",
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "abc"+str(random.randint(111111, 999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 422
    response = client.put(
        "/api/DepartmentLocations",
        headers = {"Content-Type": "application/json"}, 
        json={
        'departmentLocationID':11150675,
        "storeLocationID": 38,
        "departmentID": 1022,
        "posDepartmentCode": "abc"+str(random.randint(111111, 999999)),
        "posSyncStatusID": 0,
        "storeLocationTaxID": 0,
        "storeLocationSalesRestrictionID": 0,
        "posDepartmentDescription": "abc"+str(random.randint(111111, 999999)),
        "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
        "updateDescInEDIInvoiceFlag": True,
        "updateSellingPriceInEDIInvoiceFlag": True,
        "isBlueLaw1Enabled": True,
        "isBlueLaw2Enabled": True,
        "profitPercent": 0,
        "deptProductCode": 0,
        "isUpdateTaxandRestrication": True,
        "salesRestrictionDescription": "string",
        "salesRestrictFlag": True,
        "prohibitDiscountFlag": True,
        "taxStrategyDescription": "string",
        "countyTax": 0,
        "stateTax": 0,
        "cityTax": 0,
        "storeName": "string",
        "posSystemCD": "string",
        "posSyncStatusCode": "string",
        "userName": "string"
        }
        )
    assert response.status_code == 404
    
    response = client.put(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
            "departmentLocationID": 11150706,
            "storeLocationID": 38,
            "departmentID": 1022,
            "posDepartmentCode": "abc731963",
            "posSyncStatusID": 0,
            "storeLocationTaxID": 0,
            "storeLocationSalesRestrictionID": 0,
            "posDepartmentDescription": "abc",
            "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
            "updateDescInEDIInvoiceFlag": True,
            "updateSellingPriceInEDIInvoiceFlag": True,
            "isBlueLaw1Enabled": True,
            "isBlueLaw2Enabled": True,
            "profitPercent": 0,
            "deptProductCode": 0,
            "isUpdateTaxandRestrication": True,
            "salesRestrictionDescription": "string",
            "salesRestrictFlag": True,
            "prohibitDiscountFlag": True,
            "taxStrategyDescription": "string",
            "countyTax": 0,
            "stateTax": 0,
            "cityTax": 0,
            "storeName": "string",
            "posSystemCD": "string",
            "posSyncStatusCode": "string",
            "userName": "string"
        }
        )
    temp=response.json()
    print(temp)
    
    assert (temp['status_code'])==403
    
    response = client.put(
        "/api/DepartmentLocation",
        headers = {"Content-Type": "application/json"}, 
        json={
            "departmentLocationID":11150706,
            "storeLocationID": 38,
            "departmentID": 1022,
            "posDepartmentCode": "abcd",
            "posSyncStatusID": 0,
            "storeLocationTaxID": 0,
            "storeLocationSalesRestrictionID": 0,
            "posDepartmentDescription": "abc",
            "currentAsOfDateTime": "2023-01-09T06:53:01.988Z",
            "updateDescInEDIInvoiceFlag": True,
            "updateSellingPriceInEDIInvoiceFlag": True,
            "isBlueLaw1Enabled": True,
            "isBlueLaw2Enabled": True,
            "profitPercent": 0,
            "deptProductCode": 0,
            "isUpdateTaxandRestrication": True,
            "salesRestrictionDescription": "string",
            "salesRestrictFlag": True,
            "prohibitDiscountFlag": True,
            "taxStrategyDescription": "string",
            "countyTax": 0,
            "stateTax": 0,
            "cityTax": 0,
            "storeName": "string",
            "posSystemCD": "string",
            "posSyncStatusCode": "string",
            "userName": "string"
        })
    temp=response.json()
    print(temp)
    
    assert (temp['status_code'])==403
    
    
    
def test_DepartmentLocation_delete():
    response = client.delete("/api/DepartmentLocation?id=11150690")
    assert response.status_code == 200
    
    response = client.delete("/api/DepartmentLocations?id=11150690")
    assert response.status_code == 404
    response = client.delete("/api/DepartmentLocation?id=11as150690")
    assert response.status_code == 500