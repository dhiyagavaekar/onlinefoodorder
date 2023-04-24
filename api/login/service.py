from models import login_models
from fastapi import FastAPI, Body, Depends
from . import jwt_handler
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status
from common import helper as common_helper

from . import service as department_service

login_routes = APIRouter(prefix='/api')

users = []


@login_routes.post("/user/signup", tags=["user"])
def user_signup(user: login_models.UserSchema = Body(default=None)):
    users.append(user) # replace with db call, making sure to hash the password first
    return jwt_handler.signJWT(user.email)

def check_user(data:login_models.UserLoginSchema):
    for user in users:
        if user.email == data.email and  user.password == data.password:
            return True
        return False


@login_routes.post("/user/login", tags=["user"])
def user_login(user: login_models.UserLoginSchema = Body(default=None)):
    if check_user(user):
        return jwt_handler.signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
