from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as payment_service
from schema import fooditem_schema
payment_routes = APIRouter()
# ,  dependencies=[Depends(jwt_bearer.JWTBearer())]

@payment_routes.get(
    "/get_paytmentoforder", tags=['payment']
)
def Get_paytment_of_order(Session = Depends(common_helper.get_session)):
    return payment_service.get_paytment_of_order(Session)