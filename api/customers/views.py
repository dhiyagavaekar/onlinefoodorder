

from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as customers_service
from schema import order_schema,customers_schema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

customers_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]

@customers_routes.post("/customer-Signup", response_model=customers_schema.Token,tags=["customers"])
def Signup(user: customers_schema.UserCreate, db: Session = Depends(common_helper.get_session)):
    return customers_service.signup(user,db)

@customers_routes.post("/customer-Login", response_model=customers_schema.Token,tags=["customers"])
def Login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return customers_service.login(form_data,db)

@customers_routes.post("/getcustomer-with-token", tags=["customers"])
def Create_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return customers_service.create_token(form_data,db)


# @customers_routes.get("/users/me",tags=["customers"])
# def read_current_user(current_user: dict = Depends(customers_service.get_current_user)):
#     return current_user


@customers_routes.get(
    "/Allcustomers",  dependencies=[Depends(jwt_bearer.JWTBearer())],  tags=['customers']
)
def customers_read(Session = Depends(common_helper.get_session)):
    return customers_service.read_customers(Session)

@customers_routes.get(
    "/getorderdetailbyid",  tags=['customers']
)
def Getorderdetailbyid(orderid,Session = Depends(common_helper.get_session)):
    return customers_service.getOrderDetailbyId(orderid,Session)

@customers_routes.put(
    "/orderupdate/{id}",
    response_model=order_schema.Order,
    status_code=status.HTTP_201_CREATED,tags=["customers"]
)
def Orderupdate(
        id, customerid,order_update:order_schema.OrderUpdate, Session=Depends(common_helper.get_session)
    ):
    return customers_service.orderUpdate(id, customerid,order_update,Session)

@customers_routes.post(
    "/createorder/{id}",\
        response_model=order_schema.Order,
    status_code=status.HTTP_201_CREATED,tags=["customers"]
)
def Createorder(id,order:order_schema.OrderCreate,Session = Depends(common_helper.get_session)): 
    return  customers_service.createOrder(id,order,Session)

@customers_routes.delete(
    "/order-delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,tags=["customers"]
)
def Delete_order(orderid:int, Session = Depends(common_helper.get_session)):
    return customers_service.deleteOrder(orderid,Session) 



