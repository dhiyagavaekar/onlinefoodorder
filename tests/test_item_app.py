import sys
sys.path.insert(0, '..')
from main import app
import main
from fastapi.testclient import TestClient
import random

# Declaring test client
client = TestClient(app)


def test_Item_Get_All_By_Price_GroupID():
    response = client.get("/api/item/GetAllItemsByPriceGroupID/44975932")
    assert response.status_code == 200
    response = client.put("/api/item/GetAllItemsByPriceGroupID/44975932")
    assert response.status_code == 405
    response = client.get("/api/item/GetAllItemsByPriceGroupIDDD/44975932")
    assert response.status_code == 404
    response = client.get("/api/item/GetAllItemsByPriceGroupID/xdccds")
    assert response.status_code == 500

def test_get_items():
    response = client.get("/api/items?page=1&DepartmentIDs=25449,23128&StoreLocationIDs=996,1132,1135,1136&imit=50")
    assert response.status_code == 200
    response = client.get("/api/items?page=1&DepartmentIDs=25449,23128&StoreLocationIDs=&imit=50&CompanyIDs=7,13")
    assert response.status_code == 200
    response = client.get("/api/items?DepartmentIDs=25449%2C23128&StoreLocationIDs=38%2C45&page=1&limit=50")
    assert response.status_code == 200
    response = client.get("/api/items?page=1&limit=50&POSCodeOrDescription=marl&SellPrice=6.99&Operator='='&StoreLocationIDs=45")
    assert response.status_code == 200
    response = client.get("/api/items?page=1&limit=50&POSCodeOrDescription=marl&SellPrice=6&Operator='>'&StoreLocationIDs=45")
    assert response.status_code == 200
    response = client.get("/api/items?page=1&limit=50&POSCodeOrDescription=marl&SellPrice=6&Operator=%3E&StoreLocationIDs=45")
    assert response.status_code == 200
    response = client.get("/api/items?POSCodeOrDescription=BOTTLE&page=1&DepartmentIDs=25449,23128&StoreLocationIDs=996,1132,1135,1136")
    assert response.status_code == 200
    response = client.get("/api/items?SellPrice=14&POSCodeOrDescription=BOTTLE&page=1&DepartmentIDs=25449,23128&StoreLocationIDs=996,1132,1135,1136&Operator=>")
    assert response.status_code == 200
    response = client.get("/api/items?DepartmentIDs=23128&SellPrice=8&POSCodeOrDescription=BOTTLE&page=1&DepartmentIDs=25449,23128&StoreLocationIDs=996,1132,1135,1136&Operator=<")
    assert response.status_code == 200
    response = client.get("/api/items?DepartmentIDs=23128&SellPriceBetween=0,20&POSCodeOrDescription=BOTTLE&page=1&DepartmentIDs=25449,23128&StoreLocationIDs=996,1132,1135,1136&Operator=<")
    assert response.status_code == 200
    response = client.get("/api/items?SellPriceBetween=0,20&CompanyIDs=13,7&POSCodeOrDescription=BOTTLE&page=1")
    assert response.status_code == 200
    response = client.get("/api/items?SellPrice=8&CompanyIDs=13,7&POSCodeOrDescription=BOTTLE&page=1&Operator=<")
    assert response.status_code == 200
    response = client.get("/api/items?IsMultipack=true&SellPrice=8&POSCodeOrDescription=BOTTLE&page=1")
    assert response.status_code == 200
    response = client.get("/api/items/?page=1&StoreLocationIDs=38&VendorIDs=212,205,199")
    assert response.status_code == 200
    response = client.get("/api/items/?StoreLocationIDs=38&POSCodeOrDescription=03400047103")
    assert response.status_code == 200
    response = client.get("/api/items?POSCodeOrDescription=123&DepartmentIDs=25449,23128&page=1&limit=10")
    assert response.status_code == 200
    response = client.get("/api/items?POSCodeOrDescription=marl&DepartmentIDs=25449,23128&page=1&limit=10")
    assert response.status_code == 200
    response = client.get("/api/items?POSCodeOrDescription=BOTTLE&DepartmentIDs=25449,23128&page=1&limit=10")
    assert response.status_code == 200
    response = client.get("/api/items?POSCodeOrDescription=123&page=1&limit=10")
    assert response.status_code == 200
    response = client.get("/api/items?POSCodeOrDescription=marl&page=1&limit=10")
    assert response.status_code == 200
    response = client.get("/api/items?POSCodeOrDescription=BOTTLE&page=1&limit=10")
    assert response.status_code == 200

    response = client.get("/api/items/?page=1&size=50&GroupIDs=63538476,63539477,63540478,63541479,63551489,63562500")
    assert response.status_code == 200
    response = client.get("/api/items/?page=1&size=50&GroupIDs=63538476,63539477,63540478,63541479,63551489,63562500&VendorIDs=3533,3521,4644")
    assert response.status_code == 200
    response = client.get("/api/items/?page=1&size=50")
    assert response.status_code == 200
    
    response = client.put("/api/items?page=1&DepartmentIDs=25449,23128&StoreLocationIDs=996,1132,1135,1136&imit=50")
    assert response.status_code == 405
    response = client.get("/api/itemh?page=1&DepartmentIDs=25449,23128&StoreLocationIDs=996,1132,1135,1136&imit=50")
    assert response.status_code == 404
    response = client.get("/api/items?POSCodeOrDescription=123&DepartmentIDs=1%2C2&VendorIDs=3%2C4&GroupIDs=5%2C6&IsMultipack=true&SellPrice=2.50&Operator=%3E&SellPriceBetween=true&StoreLocationIDs=7%2C8&page=1&limit=10")
    assert response.status_code == 500
    response = client.get("/api/items?POSCodeOrDescription=BOTTLE&DepartmentIDs=asdf&VendorIDs=asd&page=1000000000&limit=1000000000")
    assert response.status_code == 500
    


def test_Item_Get_By_ID():
    response = client.post("/api/item/getByID",
                           headers={"Content-Type": "application/json"},
                           json={"companyID": 17,
                                 "posCodeOrDesc": "marl", "sellingUnitStart": None, "sellingUnitEnd": None,
                                 "unitsInCaseStart": None, "unitsInCaseEnd": None, "sellingPriceStart": None,
                                 "sellingPriceEnd": None, "inventoryValuePriceStart": None, "inventoryValuePriceEnd": None,
                                 "currentInventoryStart": None, "currentInventoryEnd": None,
                                 "pMStartCriteria": None, "pmEndCriteria": None, "locationCriteria": 996, "vendorCriteria": "", "department": "",
                                 "posSyncStatus": "", "isShowPricing": False, "isClick": True, "isOnWatchList": None, "priceGroup": None,
                                 "isMultipack": False, "isActive": None, "searchBy": None, "isShowMultiPackPricing": False, "isShowDetails": False}
                           )
    assert response.status_code == 200
    response = client.post("/api/item/getByID",
                           headers={"Content-Type": "application/json"},
                           json={"companyID": "scjdcnecj",
                                 "posCodeOrDesc": "marl", "sellingUnitStart": None, "sellingUnitEnd": None,
                                 "unitsInCaseStart": None, "unitsInCaseEnd": None, "sellingPriceStart": None,
                                 "sellingPriceEnd": None, "inventoryValuePriceStart": None, "inventoryValuePriceEnd": None,
                                 "currentInventoryStart": None, "currentInventoryEnd": None,
                                 "pMStartCriteria": None, "pmEndCriteria": None, "locationCriteria": 996, "vendorCriteria": "", "department": "",
                                 "posSyncStatus": "", "isShowPricing": False, "isClick": True, "isOnWatchList": None, "priceGroup": None,
                                 "isMultipack": False, "isActive": None, "searchBy": None, "isShowMultiPackPricing": False, "isShowDetails": False}
                           )
    assert response.status_code == 422
    response = client.put("/api/item/getByID",
                          headers={"Content-Type": "application/json"},
                          json={"companyID": 17,
                                "posCodeOrDesc": "marl", "sellingUnitStart": None, "sellingUnitEnd": None,
                                "unitsInCaseStart": None, "unitsInCaseEnd": None, "sellingPriceStart": None,
                                "sellingPriceEnd": None, "inventoryValuePriceStart": None, "inventoryValuePriceEnd": None,
                                "currentInventoryStart": None, "currentInventoryEnd": None,
                                "pMStartCriteria": None, "pmEndCriteria": None, "locationCriteria": 996, "vendorCriteria": "", "department": "",
                                "posSyncStatus": "", "isShowPricing": False, "isClick": True, "isOnWatchList": None, "priceGroup": None,
                                "isMultipack": False, "isActive": None, "searchBy": None, "isShowMultiPackPricing": False, "isShowDetails": False}
                          )
    assert response.status_code == 405
    response = client.post("/api/item/getByIDDF",
                           headers={"Content-Type": "application/json"},
                           json={"companyID": 17,
                                 "posCodeOrDesc": "marl", "sellingUnitStart": None, "sellingUnitEnd": None,
                                 "unitsInCaseStart": None, "unitsInCaseEnd": None, "sellingPriceStart": None,
                                 "sellingPriceEnd": None, "inventoryValuePriceStart": None, "inventoryValuePriceEnd": None,
                                 "currentInventoryStart": None, "currentInventoryEnd": None,
                                 "pMStartCriteria": None, "pmEndCriteria": None, "locationCriteria": 996, "vendorCriteria": "", "department": "",
                                 "posSyncStatus": "", "isShowPricing": False, "isClick": True, "isOnWatchList": None, "priceGroup": None,
                                 "isMultipack": False, "isActive": None, "searchBy": None, "isShowMultiPackPricing": False, "isShowDetails": False}
                           )
    assert response.status_code == 404
    response = client.post("/api/item/getByID",
                           headers={"Content-Type": "application/json"},
                           json={"companyID": 17,
                                 "posCodeOrDesc": "maewddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddrl", "sellingUnitStart": None, "sellingUnitEnd": None,
                                 "unitsInCaseStart": None, "unitsInCaseEnd": None, "sellingPriceStart": None,
                                 "sellingPriceEnd": None, "inventoryValuePriceStart": None, "inventoryValuePriceEnd": None,
                                 "currentInventoryStart": None, "currentInventoryEnd": None,
                                 "pMStartCriteria": None, "pmEndCriteria": None, "locationCriteria": 996, "vendorCriteria": "", "department": "sdssdfsaasfsaafadsddaasfd",
                                 "posSyncStatus": "", "isShowPricing": False, "isClick": True, "isOnWatchList": None, "priceGroup": None,
                                 "isMultipack": False, "isActive": None, "searchBy": 'redssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss', "isShowMultiPackPricing": False, "isShowDetails": False}
                           )
    assert response.status_code == 500


def test_add_Item():
    response = client.post("/api/item/add?updateUnitInCase=test",
                           headers={"Content-Type": "application/json"},
                           json={
                               "companyID": 17,
                               "departmentID": 21940,
                               "activeFlag": True,
                               "posCode": str(random.randint(111111111111, 999999999999)),
                               "posCodeFormatID": 0,
                               "uomid": 0,
                               "description": "sasspp"+str(random.randint(222222, 999999)),
                               "familyUPCCode": "sasspp"+str(random.randint(222222, 999999)),
                               "sellingUnits": 0,
                               "unitsInCase": 1,
                               "lastModifiedBy": "gk",
                               "createdDateTime": "2023-02-09T03:52:54.931Z",
                               "lastModifiedDateTime": "2023-02-09T03:52:54.931Z",
                               "departmentDescription": "sasspp"+str(random.randint(222222, 999999)),
                               "uomDescription": "sasspp"+str(random.randint(222222, 999999)),
                               "regularSellPrice": 0,
                               "unitCostPrice": 0,
                               "maxInventory": 0,
                               "minInventory": 0,
                               "storeLocationItemID": 0,
                               "storeLocationID": 38,
                               "storeName": "string",
                               "priceRequiredFlag": True,
                               "isFractionalQtyAllowedFlag": True,
                               "allowFoodStampsFlag": True,
                               "isItemReturnableFlag": True,
                               "isLoyaltyRedeemEligibleFlag": True,
                               "areSpecialDiscountsAllowedFlag": True,
                               "storelocationlst": "string",
                               "buyingCost": 0,
                               "sellingPrice": 0,
                               "isMultipackFlag": True,
                               "noOfBaseUnitsInCase": 10,
                               "buyDown": 0,
                               "basicBuyDown": 0,
                               "rackAllowance": 0,
                               "isMultiplier": 0,
                               "multiplierPOSCode": "string",
                               "multiplierQuantity": 0,
                               "manufacturerID": 0,
                               "manufacturerName": "string",
                               "posCodeWithCheckDigit": "string",
                               "grossProfit": 0,
                               "isTrackItem": True,
                               "inventoryValuePrice": 0,
                               "currentInventory": 0,
                               "inventoryAsOfDate": "2023-02-09T03:52:54.931Z",
                               "vendorID": 0,
                               "posCodeModifier": 0,
                               "regularPackageSellPrice": 0,
                               "mulType": "asdsd",
                               "multipackItemID": 0,
                               "isDefault": True,
                               "masterPriceBookItemID": 0,
                               "cartonPackMasterPriceBookItemID": 0,
                               "masterPriceGroupID": 0,
                               "isPromotionalUPC": 0
                           }
                           )
    assert response.status_code == 200

    response = client.put("/api/item/add?updateUnitInCase=test",
                          headers={"Content-Type": "application/json"},
                          json={
                              "companyID": 17,
                              "departmentID": 21940,
                              "activeFlag": True,
                              "posCode": str(random.randint(222222, 999999)),
                              "posCodeFormatID": 0,
                              "uomid": 0,
                              "description": "sassapp"+str(random.randint(222222, 999999)),
                              "familyUPCCode": "sassapp"+str(random.randint(222222, 999999)),
                              "sellingUnits": 0,
                              "unitsInCase": 1,
                              "lastModifiedBy": "gk",
                              "createdDateTime": "2023-02-09T03:52:54.931Z",
                              "lastModifiedDateTime": "2023-02-09T03:52:54.931Z",
                              "departmentDescription": "sassapp"+str(random.randint(222222, 999999)),
                              "uomDescription": "sassapp"+str(random.randint(222222, 999999)),
                              "regularSellPrice": 0,
                              "unitCostPrice": 0,
                              "maxInventory": 0,
                              "minInventory": 0,
                              "storeLocationItemID": 0,
                              "storeLocationID": 38,
                              "storeName": "string",
                              "priceRequiredFlag": True,
                              "isFractionalQtyAllowedFlag": True,
                              "allowFoodStampsFlag": True,
                              "isItemReturnableFlag": True,
                              "isLoyaltyRedeemEligibleFlag": True,
                              "areSpecialDiscountsAllowedFlag": True,
                              "storelocationlst": "string",
                              "buyingCost": 0,
                              "sellingPrice": 0,
                              "isMultipackFlag": True,
                              "noOfBaseUnitsInCase": 10,
                              "buyDown": 0,
                              "basicBuyDown": 0,
                              "rackAllowance": 0,
                              "isMultiplier": 0,
                              "multiplierPOSCode": "string",
                              "multiplierQuantity": 0,
                              "manufacturerID": 0,
                              "manufacturerName": "string",
                              "posCodeWithCheckDigit": "string",
                              "grossProfit": 0,
                              "isTrackItem": True,
                              "inventoryValuePrice": 0,
                              "currentInventory": 0,
                              "inventoryAsOfDate": "2023-02-09T03:52:54.931Z",
                              "vendorID": 0,
                              "posCodeModifier": 0,
                              "regularPackageSellPrice": 0,
                              "mulType": "asdsd",
                              "multipackItemID": 0,
                              "isDefault": True,
                              "masterPriceBookItemID": 0,
                              "cartonPackMasterPriceBookItemID": 0,
                              "masterPriceGroupID": 0,
                              "isPromotionalUPC": 0
                          }
                          )
    assert response.status_code == 405

    response = client.post("/api/item/add?updateUnitInCase=test",
                        headers = {"Content-Type": "application/json"},
                        json = {
  "companyID": 0,
  "departmentID": 0,
  "activeFlag": True,
  "posCode": "string",
  "posCodeFormatID": 0,
  "uomid": 0,
  "description": "string",
  "familyUPCCode": "string",
  "sellingUnits": 0,
  "unitsInCase": 0,
  "lastModifiedBy": "string",
  "createdDateTime": "2023-03-14T05:50:35.098Z",
  "lastModifiedDateTime": "2023-03-14T05:50:35.098Z",
  "departmentDescription": "string",
  "uomDescription": "string",
  "regularSellPrice": 0,
  "unitCostPrice": 0,
  "maxInventory": 0,
  "minInventory": 0,
  "storeLocationItemID": 0,
  "storeLocationID": 0,
  "storeName": "string",
  "priceRequiredFlag": True,
  "isFractionalQtyAllowedFlag": True,
  "allowFoodStampsFlag": True,
  "isItemReturnableFlag": True,
  "isLoyaltyRedeemEligibleFlag": True,
  "areSpecialDiscountsAllowedFlag": True,
  "storelocationlst": "string",
  "buyingCost": 0,
  "sellingPrice": 0,
  "isMultipackFlag": True,
  "noOfBaseUnitsInCase": 0,
  "buyDown": 0,
  "basicBuyDown": 0,
  "rackAllowance": 0,
  "isMultiplier": 0,
  "multiplierPOSCode": "string",
  "multiplierQuantity": 0,
  "manufacturerID": 0,
  "manufacturerName": "string",
  "posCodeWithCheckDigit": "string",
  "grossProfit": 0,
  "isTrackItem": True,
  "inventoryValuePrice": 0,
  "currentInventory": 0,
  "inventoryAsOfDate": "2023-03-14T05:50:35.098Z",
  "vendorID": 0,
  "posCodeModifier": 0,
  "regularPackageSellPrice": 0,
  "mulType": "string",
  "multipackItemID": 0,
  "isDefault": True,
  "masterPriceBookItemID": 0,
  "cartonPackMasterPriceBookItemID": 0,
  "masterPriceGroupID": 0,
  "isPromotionalUPC": 0
}                         )
    assert response.status_code == 500
                        


def test_item_update():
    response = client.put("/api/item/update?updateUnitInCase=test",
                          headers={"Content-Type": "application/json"},
                          json={"itemID": 5677809, "companyID": 17, "departmentID": 21940, "activeFlag": True, "posCode": "812732183223",
                                "posCodeFormatID": 0, "uomid": 0, "description": "pranay patil 2123", "familyUPCCode": "pranay patil", "sellingUnits": 0,
                                "unitsInCase": 1, "lastModifiedBy": "gk", "createdDateTime": "2023-02-09T03:52:54.931Z", "lastModifiedDateTime": "2023-02-09T03:52:54.931Z", "departmentDescription": "pranay patil",
                                "uomDescription": "pranay patil", "regularSellPrice": 0, "unitCostPrice": 0, "maxInventory": 0, "minInventory": 0, "storeLocationItemID": 0,
                                "storeLocationID": 38, "storeName": "string", "priceRequiredFlag": True, "isFractionalQtyAllowedFlag": True, "allowFoodStampsFlag": True,
                                "isItemReturnableFlag": True, "isLoyaltyRedeemEligibleFlag": True, "areSpecialDiscountsAllowedFlag": True, "storelocationlst": "string",
                                "buyingCost": 0, "sellingPrice": 0, "isMultipackFlag": True, "noOfBaseUnitsInCase": 10, "buyDown": 0, "basicBuyDown": 0,
                                "rackAllowance": 0, "isMultiplier": 0, "multiplierPOSCode": "string", "multiplierQuantity": 0, "manufacturerID": 0,
                                "manufacturerName": "string", "posCodeWithCheckDigit": "string", "grossProfit": 0, "isTrackItem": True, "inventoryValuePrice": 0,
                                "currentInventory": 0, "inventoryAsOfDate": "2023-02-09T03:52:54.931Z", "vendorID": 0, "posCodeModifier": 0, "regularPackageSellPrice": 0,
                                "mulType": "asdsd", "multipackItemID": 0, "isDefault": True, "masterPriceBookItemID": 0, "cartonPackMasterPriceBookItemID": 0, "masterPriceGroupID": 0, "isPromotionalUPC": 0}
                          )
    assert response.status_code == 200
    response = client.post("/api/item/update?updateUnitInCase=test",
                          headers={"Content-Type": "application/json"},
                          json={"itemID": 5677809, "companyID": 17, "departmentID": 21940, "activeFlag": True, "posCode": "812732183223",
                                "posCodeFormatID": 0, "uomid": 0, "description": "pranay patil 2123", "familyUPCCode": "pranay patil", "sellingUnits": 0,
                                "unitsInCase": 1, "lastModifiedBy": "gk", "createdDateTime": "2023-02-09T03:52:54.931Z", "lastModifiedDateTime": "2023-02-09T03:52:54.931Z", "departmentDescription": "pranay patil",
                                "uomDescription": "pranay patil", "regularSellPrice": 0, "unitCostPrice": 0, "maxInventory": 0, "minInventory": 0, "storeLocationItemID": 0,
                                "storeLocationID": 38, "storeName": "string", "priceRequiredFlag": True, "isFractionalQtyAllowedFlag": True, "allowFoodStampsFlag": True,
                                "isItemReturnableFlag": True, "isLoyaltyRedeemEligibleFlag": True, "areSpecialDiscountsAllowedFlag": True, "storelocationlst": "string",
                                "buyingCost": 0, "sellingPrice": 0, "isMultipackFlag": True, "noOfBaseUnitsInCase": 10, "buyDown": 0, "basicBuyDown": 0,
                                "rackAllowance": 0, "isMultiplier": 0, "multiplierPOSCode": "string", "multiplierQuantity": 0, "manufacturerID": 0,
                                "manufacturerName": "string", "posCodeWithCheckDigit": "string", "grossProfit": 0, "isTrackItem": True, "inventoryValuePrice": 0,
                                "currentInventory": 0, "inventoryAsOfDate": "2023-02-09T03:52:54.931Z", "vendorID": 0, "posCodeModifier": 0, "regularPackageSellPrice": 0,
                                "mulType": "asdsd", "multipackItemID": 0, "isDefault": True, "masterPriceBookItemID": 0, "cartonPackMasterPriceBookItemID": 0, "masterPriceGroupID": 0, "isPromotionalUPC": 0}
                          )
    assert response.status_code == 405
    response = client.put("/api/item/updatess?updateUnitInCase=test",
                          headers={"Content-Type": "application/json"},
                          json={"itemID": 5677809, "companyID": 17, "departmentID": 21940, "activeFlag": True, "posCode": "812732183223",
                                "posCodeFormatID": 0, "uomid": 0, "description": "pranay patil 2123", "familyUPCCode": "pranay patil", "sellingUnits": 0,
                                "unitsInCase": 1, "lastModifiedBy": "gk", "createdDateTime": "2023-02-09T03:52:54.931Z", "lastModifiedDateTime": "2023-02-09T03:52:54.931Z", "departmentDescription": "pranay patil",
                                "uomDescription": "pranay patil", "regularSellPrice": 0, "unitCostPrice": 0, "maxInventory": 0, "minInventory": 0, "storeLocationItemID": 0,
                                "storeLocationID": 38, "storeName": "string", "priceRequiredFlag": True, "isFractionalQtyAllowedFlag": True, "allowFoodStampsFlag": True,
                                "isItemReturnableFlag": True, "isLoyaltyRedeemEligibleFlag": True, "areSpecialDiscountsAllowedFlag": True, "storelocationlst": "string",
                                "buyingCost": 0, "sellingPrice": 0, "isMultipackFlag": True, "noOfBaseUnitsInCase": 10, "buyDown": 0, "basicBuyDown": 0,
                                "rackAllowance": 0, "isMultiplier": 0, "multiplierPOSCode": "string", "multiplierQuantity": 0, "manufacturerID": 0,
                                "manufacturerName": "string", "posCodeWithCheckDigit": "string", "grossProfit": 0, "isTrackItem": True, "inventoryValuePrice": 0,
                                "currentInventory": 0, "inventoryAsOfDate": "2023-02-09T03:52:54.931Z", "vendorID": 0, "posCodeModifier": 0, "regularPackageSellPrice": 0,
                                "mulType": "asdsd", "multipackItemID": 0, "isDefault": True, "masterPriceBookItemID": 0, "cartonPackMasterPriceBookItemID": 0, "masterPriceGroupID": 0, "isPromotionalUPC": 0}
                          )
    assert response.status_code == 404
    response = client.put("/api/item/update?updateUnitInCase=test",
                          headers={"Content-Type": "application/json"},
                          json={"itemID": "asdf", "companyID": "yuj", "departmentID": 21940, "activeFlag": True, "posCode": "812732183553", "posCodeFormatID": 0,
                                "uomid": 0, "description": "FastApi", "familyUPCCode": "pranay patil", "sellingUnits": 0, "unitsInCase": 1, "lastModifiedBy": "gk",
                                "createdDateTime": "2023-02-09T03:52:54.931Z", "lastModifiedDateTime": "2023-02-09T03:52:54.931Z", "departmentDescription": "pranay patil",
                                "uomDescription": "pranay patil", "regularSellPrice": 0, "unitCostPrice": 0, "maxInventory": 0, "minInventory": 0, "storeLocationItemID": 0,
                                "storeLocationID": 38, "storeName": "string", "priceRequiredFlag": True, "isFractionalQtyAllowedFlag": True, "allowFoodStampsFlag": True, "isItemReturnableFlag": True,
                                "isLoyaltyRedeemEligibleFlag": True, "areSpecialDiscountsAllowedFlag": True, "storelocationlst": "string", "buyingCost": 0, "sellingPrice": 0, "isMultipackFlag": True,
                                "noOfBaseUnitsInCase": 10, "buyDown": 0, "basicBuyDown": 0, "rackAllowance": 0, "isMultiplier": 0, "multiplierPOSCode": "string", "multiplierQuantity": 0, "manufacturerID": 0,
                                "manufacturerName": "string", "posCodeWithCheckDigit": "string", "grossProfit": 0, "isTrackItem": True, "inventoryValuePrice": 0, "currentInventory": 0,
                                "inventoryAsOfDate": "2023-02-09T03:52:54.931Z", "vendorID": 0, "posCodeModifier": 0, "regularPackageSellPrice": 0, "mulType": "asdsd",
                                "multipackItemID": 0, "isDefault": True, "masterPriceBookItemID": 0, "cartonPackMasterPriceBookItemID": 0, "masterPriceGroupID": 0, "isPromotionalUPC": 0}
                          )
    assert response.status_code == 422
    response = client.put("/api/item/update?updateUnitInCase=test",
                          headers={"Content-Type": "application/json"},
                          json={"itemID": 0, "companyID": 0, "departmentID": 0, "activeFlag": True, "posCode": "string", "posCodeFormatID": 0,
                                "uomid": 0, "description": "string", "familyUPCCode": "string", "sellingUnits": 0, "unitsInCase": 0, "lastModifiedBy": "string",
                                "createdDateTime": "2023-02-09T07:54:29.378Z", "lastModifiedDateTime": "2023-02-09T03:52:54.931Z", "departmentDescription": "string",
                                "uomDescription": "pranay patil", "regularSellPrice": 0, "unitCostPrice": 0, "maxInventory": 0, "minInventory": 0, "storeLocationItemID": 0,
                                "storeLocationID": 0, "storeName": "string", "priceRequiredFlag": True, "isFractionalQtyAllowedFlag": True, "allowFoodStampsFlag": True, "isItemReturnableFlag": True,
                                "isLoyaltyRedeemEligibleFlag": True, "areSpecialDiscountsAllowedFlag": True, "storelocationlst": "string", "buyingCost": 0, "sellingPrice": 0, "isMultipackFlag": True,
                                "noOfBaseUnitsInCase": 0, "buyDown": 0, "basicBuyDown": 0, "rackAllowance": 0, "isMultiplier": 0, "multiplierPOSCode": "string", "multiplierQuantity": 0, "manufacturerID": 0,
                                "manufacturerName": "string", "posCodeWithCheckDigit": "string", "grossProfit": 0, "isTrackItem": True, "inventoryValuePrice": 0, "currentInventory": 0,
                                "inventoryAsOfDate": "2023-02-09T03:52:54.931Z", "vendorID": 0, "posCodeModifier": 0, "regularPackageSellPrice": 0, "mulType": "asdsd",
                                "multipackItemID": 0, "isDefault": True, "masterPriceBookItemID": 0, "cartonPackMasterPriceBookItemID": 0, "masterPriceGroupID": 0, "isPromotionalUPC": 0}
                          )
    assert response.status_code == 500
    
def test_items_bulk_update():
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json=
{
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "Department_id",
      "storelst": "996,1233",
      "value": "1022"
    }
  ]
}
                           )

    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json=
{
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "CurrentInv",
      "storelst": "996",
      "value": "125"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json=
{
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "SellingPrice",
      "storelst": "996",
      "value": "123"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json= 
{
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "Buying",
      "storelst": "996",
      "value": "123"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json=
{
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "SellingUnits",
      "storelst": "996",
      "value": "126"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json=
{
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "UnitOfMeasurement",
      "storelst": "996",
      "value": "1"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json=
{
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "UnitsInCase",
      "storelst": "996",
      "value": "128"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json=
{
  "itemlst": "4810933",
  "columnList": [
    {
      "columnName": "PriceGroup",
      "storelst": "996,1233",
      "value": "1222"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json={
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "POSSyncStatus",
      "storelst": "996",
      "value": "1"
    }
  ]
}
                           )
    assert response.status_code == 200  
    response = client.post("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json={
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "POSSyncStatus",
      "storelst": "996",
      "value": "1"
    }
  ]
}
                           )
    assert response.status_code == 405 
    response = client.put("/api/items/bulk-updatee",
                           headers={"Content-Type": "application/json"},
                           json={
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "PriceGroup",
      "storelst": "996",
      "value": "1222"}
  ]
}
                           )
   
    assert response.status_code == 404
    
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json={
  "itemlst": "4810933",
  "columnList": [
    {
      "columnName": "POSSyncStatus",
      "storelst": "996,123",
      "value": "1"
    }
  ]
}
                           )
    temp = response.json()
    assert temp['status_code'] == 404
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json={
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "PriceGroup",
      "storelst": "996",
      "value": "1222"}
  ]
}
                           )
   
    temp = response.json()
    assert temp['status_code'] == 404
    
    response = client.put("/api/items/bulk-update",
                           headers={"Content-Type": "application/json"},
                           json={
  "itemlst": "4647817,4647816,4647750",
  "columnList": [
    {
      "columnName": "POSSyncStatus",
      "storelst": "asd",
      "value": "1"
    }
  ]
}
                           )
    assert response.status_code == 500
    
    

