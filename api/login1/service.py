from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from schema import userlogin1_schema
from models import userlogin1_models
from common import helper as common_helper


login_routes1 = APIRouter(prefix='/api')

SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

@login_routes1.post("/signup1", response_model=userlogin1_schema.Token)
def signup(user: userlogin1_schema.UserCreate, db: Session = Depends(common_helper.get_session)):
    db_user = db.query(userlogin1_models.Users1).filter(userlogin1_models.Users1.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = userlogin1_models.Users1(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@login_routes1.post("/login1", response_model=userlogin1_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(common_helper.get_session)):
    user = db.query(userlogin1_models.Users1).filter(userlogin1_models.Users1.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

