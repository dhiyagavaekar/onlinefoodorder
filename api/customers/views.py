

from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as customers_service
from schema import order_schema,customers_schema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.registration_login import service as reg_service
from jose import jwt, JWTError


customers_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]


@customers_routes.get("/customersbyid",tags=["customers"])
def CustomersbyId(db: Session = Depends(common_helper.get_session), token: str = Depends(reg_service.oauth2_scheme) ):
    middleware = jwt.decode(token,reg_service.SECRET_KEY,reg_service.ALGORITHM)
    username = middleware.get("sub")
    password = middleware.get("password")
    return customers_service.get_customer_details(username,password,db)

# dependencies=[Depends(customers_service.check_active)]
@customers_routes.get(
    "/Allcustomers",  tags=['customers']
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

@customers_routes.delete(
    "/order-softdelete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,tags=["customers"]
)
def SoftDelete_order(orderid:int, Session = Depends(common_helper.get_session)):
    return customers_service.softdelete_order(orderid,Session) 


