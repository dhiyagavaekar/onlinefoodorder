from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as restaurent_service
from schema import fooditem_schema
restaurent_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]

@restaurent_routes.get(
    "/getallrestaurents", tags=['restaurent']
)
def Getallrestaurents(Session = Depends(common_helper.get_session)):
    return restaurent_service.getallrestaurents(Session)

@restaurent_routes.post(
    "/addfooditem/{id}",\
        response_model=fooditem_schema.Fooditem,
    status_code=status.HTTP_201_CREATED,tags=["fooditems"]
)
def Addfooditem(id,addfood:fooditem_schema.FooditemCreate,Session = Depends(common_helper.get_session)): 
    return  restaurent_service.addfooditem(id,addfood,Session)

@restaurent_routes.put(
    "/fooditemupdate/{id}",
    response_model=fooditem_schema.Fooditem,
    status_code=status.HTTP_201_CREATED,tags=["fooditems"]
)
def Fooditemupdate(
        fooditemid,restaurentid,order_update:fooditem_schema.FooditemUpdate, Session=Depends(common_helper.get_session)
    ):
    return restaurent_service.fooditemupdate(fooditemid,restaurentid,order_update,Session)

@restaurent_routes.delete(
    "/fooditem-delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,tags=["fooditems"]
)
def Delete_fooditem(restaurentid,fooditemid:int, Session = Depends(common_helper.get_session)):
    return restaurent_service.delete_fooditem(restaurentid,fooditemid,Session) 

