from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as order_service
from schema import fooditem_schema
order_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]
@order_routes.get(
    "/read_orders", tags=['orders']
)
def Read_orders(Session = Depends(common_helper.get_session)):
    return order_service.read_orders(Session)

@order_routes.get(
    "/read_orderbyid", tags=['orders']
)
def Read_orderbyid(orderid:int,Session = Depends(common_helper.get_session)):
    return order_service.read_OrderbyId(orderid,Session)

