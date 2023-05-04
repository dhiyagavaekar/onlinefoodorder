from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as delivery_service
from schema import deliverystaff_schema
from api.registration_login import service as reg_service
from jose import jwt, JWTError


delivery_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

@delivery_routes.get("/deliverystaff/",tags=["deliverystaff"])
def DeliverStaffbyId(db: Session = Depends(common_helper.get_session), token: str = Depends(reg_service.oauth2_scheme) ):
    middleware = jwt.decode(token,reg_service.SECRET_KEY,reg_service.ALGORITHM)
    username = middleware.get("sub")
    password = middleware.get("password")
    return delivery_service.get_deliverystaff_details(username,password,db)

@delivery_routes.get(
    "/CustomerDelivery/Details", tags=['deliverystaff']
)
def Read_deliverydetails(restaurentid:int,Session = Depends(common_helper.get_session)):
    return delivery_service.readCustomerDeliveryDetails(restaurentid,Session)



@delivery_routes.get(
    "/delivery/status", tags=['deliverystaff']
)
def Get_deliverystatus(status:str,Session = Depends(common_helper.get_session)):
    return delivery_service.getDeliveryofSpecificStatus(status,Session)

@delivery_routes.get(
    "/delivery/all/status", tags=['deliverystaff']
)
def Get_deliveryallstatus(Session = Depends(common_helper.get_session)):
    return delivery_service.getDeliveryofAllStatus(Session)

