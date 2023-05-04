from models import login_models
from fastapi import FastAPI, Body, Depends,HTTPException
from . import jwt_handler
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from models import userlogin1_models
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from schema import userlogin1_schema
from models import userlogin1_models,customers_models
from . import jwt_bearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/getcustomer-with-token")
SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

from . import service as department_service

login_routes = APIRouter(prefix='/api')

users = []

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


    return customers    
@login_routes.post("/customer/signup", tags=["login-customers"])
def user_signup(user: userlogin1_schema.UserCreate,db: Session = Depends(common_helper.get_session)):
    db_user = db.query(customers_models.Customers).filter(customers_models.Customers.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = customers_models.Customers(email=user.email, password=hashed_password,firstname=user.firstname,\
        lastname=user.lastname,address=user.address,city=user.city,state=user.state,mobile_no=user.mobile_no,created_at=user.created_at,updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    # return {"access_token": access_token, "token_type": "bearer"}
    return jwt_handler.signJWT(user.email)

@login_routes.post("/customer/login", tags=["login-customers"])
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    user = db.query(customers_models.Customers).filter(customers_models.Customers.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    data = {
        "sub": user.email,
        "customerId": user.customerId,
        "firstname": user.firstname,
        "email":user.email
        
    }
    access_token = create_access_token(data=data)
    return jwt_handler.signJWT(access_token)

@login_routes.post("/getcustomer-with-token", tags=["login-customers"])
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):

    # user = authenticate_user(db, form_data.username, form_data.password)
    user = db.query(customers_models.Customers).filter(customers_models.Customers.email == form_data.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        
        "customerId": user.customerId,
        "firstname": user.firstname,
        "lastname":user.lastname,
        "email": user.email,
        "mobile_no.":user.mobile_no
        
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    result = {"CustomerData":access_token_data,"access_token": access_token}
    return jwt_handler.signJWT(result)

# @login_routes.get("/customersbyid", tags=["login-customers"])
# def CustomersbyId(token: str, db: Session = Depends(common_helper.get_session)):

#     try:
#         payload = jwt_handler.check_active(token)
#         print(payload)
#     except ValueError:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     customerId = payload.get("customerId")
#     customers =\
#         db.query(
#             customers_models.Customers
#         ).filter(customers_models.Customers.customerId==customerId).all()
    
#     return customers



