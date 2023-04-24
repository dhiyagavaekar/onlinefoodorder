from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as delivery_service
from schema import fooditem_schema
delivery_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]
@delivery_routes.get(
    "/read_deliverydetails", tags=['delivery']
)
def Read_deliverydetails(restaurentid:int,Session = Depends(common_helper.get_session)):
    return delivery_service.read_deliverydetails(restaurentid,Session)

@delivery_routes.get(
    "/get_delivery_of_status", tags=['delivery']
)
def Get_deliverystatus(status:str,Session = Depends(common_helper.get_session)):
    return delivery_service.get_deliveryofstatus(status,Session)

@delivery_routes.get(
    "/get_delivery_of_allstatus", tags=['delivery']
)
def Get_deliveryallstatus(Session = Depends(common_helper.get_session)):
    return delivery_service.get_deliveryofallstatus(Session)

