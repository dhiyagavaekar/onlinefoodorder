from fastapi import APIRouter
from fastapi import  Depends,APIRouter,status

from .import service as dept_location_service
from common import helper as common_helper
from . import service as department_location_service


index_routes = APIRouter()

# Helper function to get database session
@index_routes.get("/")
def root():
    return "Fast Api Department Crud"

# @index_routes.get(
#     "/DepartmentLocation"
# )
# def get_items(Session = Depends(common_helper.get_session)):
    
#     return  department_location_service.read_department_list(Session)