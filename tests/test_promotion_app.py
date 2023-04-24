"""
Test for the promotion page using fastapi.testclient.
"""
import os
import sys
sys.path.insert(0,'..')
from fastapi.testclient import TestClient
import main
import json
from main import app
 
# Declaring test client
client = TestClient(app)
 
# Test for status code for get message
def test_Promotion_ItemList_GetitemListItemscount():
    response = client.get("/api/Promotion/ItemList/GetitemListItemscount?companyID=17")
    assert response.status_code == 200
    response = client.get("/api/Promotion/ItemList/GetitemListItemscount?companyID=abcd")
    assert response.status_code == 500


def test_Promotion_ItemList_GetitemListDetailsByItemListID():
    response = client.get("/api/Promotion/ItemList/GetitemListDetailsByItemListID/?ItemListID=7623")
    assert response.status_code == 200
    response = client.get("/api/Promotion/ItemList/GetitemListDetailsByItemListID/?ItemListID=6760&StorelocationID=38")
    assert response.status_code == 200
    response = client.get("/api/Promotion/ItemList/GetitemListDetailsByItemListID/?ItemListID=asf")
    assert response.status_code == 422
    response = client.get("/api/Promotion/ItemList/GetitemListDetailsByItemListID/?ItemListID=asf&StorelocationID='asf'")
    assert response.status_code == 422

def test_Promotion_itemlist_addListItems():
    response = client.get("/api/Promotion/itemlist/addListItems?itemListId=6760&itemid=3358595&username=gk")
    assert response.status_code == 200
    response = client.get("/api/Promotion/itemlist/addListItems?itemListId=sada&itemid=asd&username=123")
    assert response.status_code == 422
    response = client.get("/api/Promotion/itemlist/addListItems?itemListId=sada&itemid=asd")
    assert response.status_code == 422
    response = client.get("/api/Promotion/itemlist/addListItems?itemListId=123&itemid=123&username='123'")
    assert response.status_code == 500

def test_Promotion_itemlist_addGroups():
    response = client.post("/api/Promotion/itemlist/addGroups?itemListId=6760&groupId=63579517&username=gk")
    assert response.status_code == 200
    response = client.post("/api/Promotion/itemlist/addGroups?itemListId=6760&groupId=2&username=gk")
    assert response.status_code == 200 
    response = client.post("/api/Promotion/itemlist/addGroups?itemListId=saad&groupId=as&username=gk")
    assert response.status_code == 422
    response = client.post("/api/Promotion/itemlist/addGroups?itemListId=saad&groupId=as")
    assert response.status_code == 422
    response = client.post("/api/Promotion/itemlist/addGroups?itemListId=6760&groupId=6357951700000000000000000000000000000000&username=as")
    assert response.status_code == 500


def test__Promotion_itemlist_getSearchItemsListItems():
    response = client.get("/api/Promotion/itemlist/getSearchItemsListItems?CompanyID=597&isShowPricing=true&posCodeOrDesc=marl&Location=697&ItemListID=10050")
    assert response.status_code == 200
    response = client.get("/api/Promotion/itemlist/getSearchItemsListItems?CompanyID=5&isShowPricing=true&posCodeOrDesc=6788&Location=697&ItemListID=fgj")
    assert response.status_code == 500
    
def test__Promotion_itemlist_GetExpiredComboCount():
    response = client.get("/api/Promotion/itemlist/GetExpiredComboCount?companyID=17&NoofDaysleft=4")
    assert response.status_code == 200
    response = client.get("/api/Promotion/itemlist/GetExpiredComboCount?companyID=aqwe&NoofDaysleft=4")
    assert response.status_code == 422
    
def test__Promotion_ComboDeal_getByCompanyId():
    response = client.get("/api/Promotion/ComboDeal/getByCompanyId/17")
    assert response.status_code == 200
    response = client.get("/api/Promotion/ComboDeal/getByCompanyId/abcd")
    assert response.status_code == 422
        
def test_Promotion_ComboDealStorelocation_GetComboStorelocationDetails():
    response = client.get("/api/Promotion/ComboDealStorelocation/GetComboStorelocationDetails?companyID=17&ComboDealID=2&UserName=gk")
    assert response.status_code == 200
    response = client.get("/api/Promotion/ComboDealStorelocation/GetComboStorelocationDetails?companyID=1&ComboDealID=6&UserName='123'")
    assert response.status_code == 500


def test_Promotion_ComboDeal_update():
    response = client.put("/api/Promotion/ComboDeal/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"comboDealID": 152,"companyID": 597,"description": "MARLBORO","itemListID": 10050}
                          )
    assert response.status_code == 200
    response = client.put("/api/Promotion/ComboDeal/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"comboDealID": "acs","companyID": 597,"description": "MARLBORO","itemListID": 10050}
                          )
    assert response.status_code == 422
    response = client.put("/api/Promotion/ComboDeal/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"comboDealID": 0,"companyID": 0,"description": "string","itemListID": 0}
                          )
    assert response.status_code == 500
    

def test_Promotion_ComboDealStorelocation_update():
    response = client.put("/api/Promotion/ComboDealStorelocation/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"comboDealStoreLocationID":267,"storeLocationID":697,"comboDealID":152,"posid":5001,"beginDate":"2021-07-02T00:00:00","endDate":"2022-12-27T00:00:00","comboAmount":0.699999988079071,"comboUnits":2,"comboPriorityTypeID":4,"posSyncStatusID":3,"manufacturerFunded":0,"retailerFunded":0,"co_funded":False,"lastModifiedBy":"gk","lastModifiedDateTime":"2023-01-11T15:29:09.694Z"}
                          )
    assert response.status_code == 200
    response = client.put("/api/Promotion/ComboDealStorelocation/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"comboDealStoreLocationID": 0,"storeLocationID": "asf","comboDealID": "fgh","posid": 0,"bginDate": "2023-02-01T12:46:13.164Z","endDate": "2023-02-01T12:46:13.164Z","comboAmount": 0,"comboUnits": 0,"comboPriorityTypeID": 0,"posSyncStatusID": 0,"manufacturerFunded": 0,"retailerFunded": 0,"co_funded": True,"lastModifiedBy": "string","lastModifiedDateTime": "2023-02-01T12:46:13.165Z"}
                          )
    assert response.status_code == 422
    response = client.put("/api/Promotion/ComboDealStorelocation/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"comboDealStoreLocationID": 0,"storeLocationID": 0,"comboDealID": 0,"posid": 0,"bginDate": "2023-02-01T12:46:13.164Z","endDate": "2023-02-01T12:46:13.164Z","comboAmount": 0,"comboUnits": 0,"comboPriorityTypeID": 0,"posSyncStatusID": 0,"manufacturerFunded": 0,"retailerFunded": 0,"co_funded": True,"lastModifiedBy": "string","lastModifiedDateTime": "2023-02-01T12:46:13.165Z"}
                          )
    assert response.status_code == 500
    
def test_Promotion_ComboDealStorelocation_delete():
    response = client.delete("/api/Promotion/ComboDealStorelocation/delete/3")
    assert response.status_code == 200
    response = client.delete("/api/Promotion/ComboDealStorelocation/delete/dfe")
    assert response.status_code == 500
    response = client.put("/api/Promotion/ComboDealStorelocation/delete/3")
    assert response.status_code == 405
    
def test_Promotion_ComboDeal_delete():
    response = client.delete("/api/Promotion/ComboDeal/delete/5")
    assert response.status_code == 200
    response = client.delete("/api/Promotion/ComboDeal/delete/dfe")
    assert response.status_code == 500
    response = client.put("/api/Promotion/ComboDeal/delete/dfe")
    assert response.status_code == 405
    response = client.delete("/api/Promotion/ComboDeal/delete/5")
    temp=response.json()
    print(temp)
    assert (temp['status_code'])==403
    
    
def test_Promotion_mixmatch_getByCompanyId():
    response = client.get("/api/Promotion/mixmatch/getByCompanyId/17")
    assert response.status_code == 200
    response = client.get("/api/Promotion/mixmatch/getByCompanyId/abcd")
    assert response.status_code == 500
    
def test_Promotion_ItemList_GetExpiredMixMatchCount():
    response = client.get("/api/Promotion/ItemList/GetExpiredMixMatchCount?companyID=17&NoofDaysleft=4")
    assert response.status_code == 200
    response = client.get("/api/Promotion/ItemList/GetExpiredMixMatchCount?companyID=as&NoofDaysleft=45")
    assert response.status_code == 500
    response = client.get("/api/Promotion/ItemList/GetExpiredMixMatchCount?companyID=as")
    assert response.status_code == 422
    
def test_Promotion_MixMatchStoreLocation_GetMixMatchStorelocationDetails():
    response = client.get("/api/Promotion/MixMatchStoreLocation/GetMixMatchStorelocationDetails?companyID=17&mixMatchID=4&Username=gk")
    assert response.status_code == 200
    response = client.get("/api/Promotion/MixMatchStoreLocation/GetMixMatchStorelocationDetails?companyID=asd&mixMatchID=4&Username=34")
    assert response.status_code == 500
    response = client.get("/api/Promotion/MixMatchStoreLocation/GetMixMatchStorelocationDetails?companyID=17&Username=hjjk")
    assert response.status_code == 422 
    
def test_Promotion_mixmatch_update():
    response = client.put("/api/Promotion/mixmatch/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"MixMatchID": 23,"CompanyID": 24,"Description": "23","ItemListID":25}
                          )
    assert response.status_code == 200
    response = client.put("/api/Promotion/mixmatch/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"MixMatchID": 0,"CompanyID": 0,"Description": "string","ItemListID":0}
                          )
    assert response.status_code == 200
    response = client.put("/api/Promotion/mixmatch/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"MixMatchID": "fg","CompanyID": "fd","Description": 4,"ItemListID": "df"}
                          )
    assert response.status_code == 422
    response = client.put("/api/Promotion/mixmatch/update",
                          headers = {"Content-Type": "application/json"}, 
                          json = {"MixMatchID": 56661,"CompanyID": 17,"Description": "2FOR109NUTS","ItemListID": 0}
                          )
    temp=response.json()
    print(temp)
    
    assert (temp['status_code'])==403
    
def test_Promotion_mixmatch_delete():
    response = client.delete("/api/Promotion/mixmatch/delete/2")
    assert response.status_code == 200
    response = client.delete("/api/Promotion/mixmatch/delete/5671")
    temp = response.json()
    print(temp)
    assert (temp['status_code'])==403
    response = client.delete("/api/Promotion/mixmatch/delete/dfg")
    assert response.status_code == 500
    
def test_Promotion_itemlist_delete():
    response = client.delete("/api/Promotion/itemlist/delete/17")
    assert response.status_code == 200
    response = client.delete("/api/Promotion/itemlist/delete/dfg")
    assert response.status_code == 500
    response = client.delete("/api/Promotion/itemlist/delete/6669")
    temp=response.json()
    print(temp)
    assert (temp['status_code'])==403
    
def test_Promotion_itemListGroup_delete():
    response = client.delete("/api/Promotion/itemListGroup/delete/15")
    assert response.status_code == 200
    response = client.delete("/api/Promotion/itemListGroup/delete/dfg")
    assert response.status_code == 500
    
def test_Promotion_itemListItem_delete():
    response = client.delete("/api/Promotion/itemListItem/delete/17")
    assert response.status_code == 200
    response = client.delete("/api/Promotion/itemListItem/delete/dfg")
    assert response.status_code == 500

def test_Promotion_MixMatchStoreLocation_delete():
    response = client.delete("/api/Promotion/MixMatchStoreLocation/delete/17")
    assert response.status_code == 200
    response = client.delete("/api/Promotion/MixMatchStoreLocation/delete/dfg")
    assert response.status_code == 500
    