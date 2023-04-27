from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as restaurent_service
from schema import fooditem_schema,restaurent_schema

restaurent_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


@restaurent_routes.post("/Signup", response_model=restaurent_schema.Token,tags=["restaurent"])
def Deliverystaff_Signup(user: restaurent_schema.UserCreate, db: Session = Depends(common_helper.get_session)):
    return restaurent_service.signup(user,db)

@restaurent_routes.post("/Login", response_model=restaurent_schema.Token,tags=["restaurent"])
def Deliverystaff_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return restaurent_service.login(form_data,db)

@restaurent_routes.post("/token", tags=["restaurent"])
def Create_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return restaurent_service.create_token(form_data,db)


@restaurent_routes.get(
    "/getallrestaurents", tags=['restaurent']
)
def Getallrestaurents(Session = Depends(common_helper.get_session)):
    return restaurent_service.getAllRestaurents(Session)

@restaurent_routes.post(
    "/addfooditem/{id}",\
        response_model=fooditem_schema.Fooditem,
    status_code=status.HTTP_201_CREATED,tags=["fooditems"]
)
def Addfooditem(id,addfood:fooditem_schema.FooditemCreate,Session = Depends(common_helper.get_session)): 
    return  restaurent_service.addFoodItem(id,addfood,Session)

@restaurent_routes.put(
    "/fooditemupdate/{id}",
    response_model=fooditem_schema.Fooditem,
    status_code=status.HTTP_201_CREATED,tags=["fooditems"]
)
def Fooditemupdate(
        fooditemid,restaurentid,order_update:fooditem_schema.FooditemUpdate, Session=Depends(common_helper.get_session)
    ):
    return restaurent_service.foodItemUpdate(fooditemid,restaurentid,order_update,Session)

@restaurent_routes.delete(
    "/fooditem-delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,tags=["fooditems"]
)
def Delete_fooditem(restaurentid,fooditemid:int, Session = Depends(common_helper.get_session)):
    return restaurent_service.delete_foodItem(restaurentid,fooditemid,Session) 

