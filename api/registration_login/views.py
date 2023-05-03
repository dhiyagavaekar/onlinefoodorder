from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from api.login import jwt_bearer
from . import service as customers_service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schema import deliverystaff_schema,restaurent_schema,customers_schema


reg_routes = APIRouter()

@reg_routes.post("/customer/Signup", response_model=customers_schema.Token,tags=["login"])
def CustomerSignup(user: customers_schema.UserCreate, db: Session = Depends(common_helper.get_session)):
    return customers_service.Customer_Signup(user,db)

@reg_routes.post("/customer/login", response_model=customers_schema.Token,tags=["login"])
def CustomerLogin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return customers_service.Customer_Login(form_data,db)

@reg_routes.post("/deliverstaff/Signup", response_model=deliverystaff_schema.Token,tags=["login"])
def Deliverystaff_Signup(user: deliverystaff_schema.UserCreate, db: Session = Depends(common_helper.get_session)):
    return customers_service.deliverystaff_signup(user,db)

@reg_routes.post("/deliverystaff/login", response_model=deliverystaff_schema.Token,tags=["login"])
def Deliverystaff_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return customers_service.deliverystaff_login(form_data,db)

@reg_routes.post("/restaurent/Signup", response_model=deliverystaff_schema.Token,tags=["login"])
def restaurent_Signup(user: restaurent_schema.UserCreate, db: Session = Depends(common_helper.get_session)):
    return customers_service.restaurent_Signup(user,db)

@reg_routes.post("/restaurent/login", response_model=deliverystaff_schema.Token,tags=["login"])
def restaurent_Login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return customers_service.restaurent_Login(form_data,db)



@reg_routes.post("/login_access_token",tags=["login"])
def Login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    return customers_service.login_access_token(form_data,db)
