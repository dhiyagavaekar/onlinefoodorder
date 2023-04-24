

from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as customers_service
from schema import order_schema

customers_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]
@customers_routes.get(
    "/Allcustomers",  dependencies=[Depends(jwt_bearer.JWTBearer())],  tags=['customers']
)
def customers_read(Session = Depends(common_helper.get_session)):
    return customers_service.read_customers(Session)

@customers_routes.get(
    "/getorderdetailbyid",  tags=['customers']
)
def Getorderdetailbyid(customerid,orderid,restaurentid:int,Session = Depends(common_helper.get_session)):
    return customers_service.getorderdetailbyid(customerid,orderid,restaurentid,Session)

@customers_routes.put(
    "/orderupdate/{id}",
    response_model=order_schema.Order,
    status_code=status.HTTP_201_CREATED,tags=["customers"]
)
def Orderupdate(
        id, customerid,order_update:order_schema.OrderUpdate, Session=Depends(common_helper.get_session)
    ):
    return customers_service.orderupdate(id, customerid,order_update,Session)

@customers_routes.post(
    "/createorder/{id}",\
        response_model=order_schema.Order,
    status_code=status.HTTP_201_CREATED,tags=["customers"]
)
def Createorder(id,order:order_schema.OrderCreate,Session = Depends(common_helper.get_session)): 
    return  customers_service.createorder(id,order,Session)

@customers_routes.delete(
    "/order-delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,tags=["customers"]
)
def Delete_order(orderid:int, Session = Depends(common_helper.get_session)):
    return customers_service.delete_order(orderid,Session) 

