from pydantic import BaseModel,validator,ValidationError
from datetime import datetime
from typing import Optional

class SignUpModel(BaseModel):
    Id : Optional[int]
    username :str
    email:str
    password :str 

    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "string",
                "email": "user@xyz.com",
                "password": "any"
            }
        }
        
class Settings(BaseModel):
    authjwt_secret_key:str = '94058304f26717be595797fc7af4eb8e5c99292a5d9ff26ae7653f35e6b37786'
  
class LoginModel(BaseModel):
    username:str
    password:str  
    
    class Config:
        orm_mode = True