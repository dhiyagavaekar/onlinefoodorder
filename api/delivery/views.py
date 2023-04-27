from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as delivery_service
from schema import deliverystaff_schema
delivery_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


@delivery_routes.post("/deliverstaff-Signup", response_model=deliverystaff_schema.Token,tags=["delivery"])
def Deliverystaff_Signup(user: deliverystaff_schema.UserCreate, db: Session = Depends(common_helper.get_session)):
    return delivery_service.deliverystaff_signup(user,db)

@delivery_routes.post("/deliverystaff-Login", response_model=deliverystaff_schema.Token,tags=["delivery"])
def Deliverystaff_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return delivery_service.deliverystaff_login(form_data,db)

@delivery_routes.post("/deliverystaff-with-token", tags=["delivery"])
def Create_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return delivery_service.create_token(form_data,db)


@delivery_routes.get(
    "/read_CustomerDeliveryDetails", tags=['delivery']
)
def Read_deliverydetails(restaurentid:int,Session = Depends(common_helper.get_session)):
    return delivery_service.readCustomerDeliveryDetails(restaurentid,Session)



@delivery_routes.get(
    "/get_delivery_of_status", tags=['delivery']
)
def Get_deliverystatus(status:str,Session = Depends(common_helper.get_session)):
    return delivery_service.getDeliveryofSpecificStatus(status,Session)

@delivery_routes.get(
    "/get_delivery_of_allstatus", tags=['delivery']
)
def Get_deliveryallstatus(Session = Depends(common_helper.get_session)):
    return delivery_service.getDeliveryofAllStatus(Session)

