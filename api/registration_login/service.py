import bcrypt
from models import customers_models,order_models,foodItems_models,orderdetails_models,restaurent_models,deliverystaff_models
from configurations import config
from fastapi import HTTPException,Response
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, status
from common import helper as common_helper
from typing import Annotated
from werkzeug.security import check_password_hash

settings=config.Settings()



SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login_access_token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# @login_routes1.post("/signup1", response_model=userlogin1_schema.Token)
def Customer_Signup(user, db):
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
    return {"access_token": access_token, "token_type": "bearer"}

# @login_routes1.post("/login1", response_model=userlogin1_schema.Token)
def Customer_Login(form_data, db):
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
    return {"access_token": access_token, "token_type": "bearer"}

def deliverystaff_signup(user, db):
    db_user = db.query(deliverystaff_models.Deliverystaff).filter(deliverystaff_models.Deliverystaff.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = deliverystaff_models.Deliverystaff(email=user.email, password=hashed_password,firstname=user.firstname,\
        lastname=user.lastname,mobile_no=user.mobile_no,created_at=user.created_at,updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# # @login_routes1.post("/login1", response_model=userlogin1_schema.Token)
def deliverystaff_login(form_data, db):
    user = db.query(deliverystaff_models.Deliverystaff).filter(deliverystaff_models.Deliverystaff.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    data = {
        "sub": user.email,
        "deliverystaffId": user.deliverystaffId,
        "firstname": user.firstname,
        "email":user.email
        
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}

def restaurent_Signup(user, db):
    db_user = db.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = restaurent_models.Restaurent(email=user.email, password=hashed_password,name=user.name,\
        address=user.address,city=user.city,state=user.state,mobile_no=user.mobile_no,created_at=user.created_at,updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# # @login_routes1.post("/login1", response_model=userlogin1_schema.Token)
def restaurent_Login(form_data, db):
    user = db.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    data = {
        "sub": user.email,
        "restaurentId": user.restaurentId,
        "name": user.name,
        "email":user.email
        
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}


def login_access_token(form_data, db):
    access_token_data = {}
    
    # Check if user exists in customers table
    user = db.query(customers_models.Customers).filter(customers_models.Customers.email == form_data.username).first() 
    print(user.password)
    if user and bcrypt.checkpw(form_data.password.encode('utf-8'), user.password.encode('utf-8')):
        access_token_data = {
            "sub": user.email,
            "customerId": user.customerId,
            "password":user.password,
            "firstname": user.firstname,
            "lastname":user.lastname,
            "email": user.email,
            "mobile_no.":user.mobile_no,
           
        }
    else:
        # Check if user exists in delivery staff table
        user = db.query(deliverystaff_models.Deliverystaff).filter(deliverystaff_models.Deliverystaff.email == form_data.username).first()
        if user and bcrypt.checkpw(form_data.password.encode('utf-8'), user.password.encode('utf-8')):
            access_token_data = {
                "sub": user.email,
                "deliverystaffId": user.deliverystaffId,
                "firstname": user.firstname,
                "lastname":user.lastname,
                "email": user.email,
                "mobile_no.":user.mobile_no,
                "password":user.password
            }
        else:
            # Check if user exists in restaurant table
            user = db.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email == form_data.username).first()
            if user and bcrypt.checkpw(form_data.password.encode('utf-8'), user.password.encode('utf-8')):
                access_token_data = {
                    "sub": user.email,
                    "password":user.password,
                    "restaurentId": user.restaurentId,
                    "firstname": user.name,
                    "email": user.email,
                    "mobile_no.":user.mobile_no,
                    "password":user.password
                }
    
    if access_token_data:
        access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"Data":access_token_data,"access_token": access_token}
    else:
        return {"error": "Invalid username or password"}



def jwt_token_middleware(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
    username = payload.get("sub")
    return payload


def verify_token(token):
    try:
        payload = jwt.decode(token, key=SECRET_KEY)
        
        print("1----------")
        return payload
    except:
        print("2----------")
        raise Exception("Wrong token")

def check_active(token: str = Depends(oauth2_scheme)):
    print("abc")
    payload = verify_token(token)
    print(payload)
    active = payload.get("Id")
    print("3----------")
    if not active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please activate your Account first",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return payload
