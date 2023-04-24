import schemas

from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper

from . import service as department_service

dummy_routes = APIRouter(prefix='/api')

@dummy_routes.get(
    "/dummy/"
)
def dept_read(Session = Depends(common_helper.get_session)):
    return department_service.read_dummy(Session)
