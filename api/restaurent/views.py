from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as restaurent_service
from schema import fooditem_schema,restaurent_schema
from api.registration_login import service as reg_service
from jose import jwt, JWTError


restaurent_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



@restaurent_routes.get("/restaurentbyId",tags=["restaurent"])
def RestaurentbyId(db: Session = Depends(common_helper.get_session),token: str = Depends(reg_service.oauth2_scheme) ):
    middleware = jwt.decode(token,reg_service.SECRET_KEY,reg_service.ALGORITHM)
    username = middleware.get("sub")
    password = middleware.get("password")
    
    return restaurent_service.get_restaurent_details(username,password,db)



@restaurent_routes.get(
    "/getallrestaurents", tags=['restaurent']
)
def Getallrestaurents(Session = Depends(common_helper.get_session)):
    return restaurent_service.getAllRestaurents(Session)

@restaurent_routes.post(
    "/addfooditem/",\
        response_model=fooditem_schema.Fooditem,
    status_code=status.HTTP_201_CREATED,tags=["fooditems"]
)
def Addfooditem(fooditem:fooditem_schema.FooditemCreate,Session = Depends(common_helper.get_session), token: str = Depends(reg_service.oauth2_scheme),\
    ): 
    middleware_username=reg_service.jwt_token_middleware(token)
    return  restaurent_service.addFoodItem(fooditem,Session,middleware_username)

@restaurent_routes.put(
    "/fooditemupdate/{id}",
    response_model=fooditem_schema.Fooditem,
    status_code=status.HTTP_201_CREATED,tags=["fooditems"]
)
def Fooditemupdate(
        id,order_update:fooditem_schema.FooditemUpdate, Session=Depends(common_helper.get_session), token: str = Depends(reg_service.oauth2_scheme)
    ):
    middleware_username=reg_service.jwt_token_middleware(token)
    return restaurent_service.foodItemUpdate(id,order_update,Session,middleware_username)

@restaurent_routes.delete(
    "/fooditem-delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,tags=["fooditems"]
)
def Delete_fooditem(fooditemid:int, Session = Depends(common_helper.get_session), token: str = Depends(reg_service.oauth2_scheme)):
    middleware_username=reg_service.jwt_token_middleware(token)
    return restaurent_service.delete_foodItem(fooditemid,Session,middleware_username) 

