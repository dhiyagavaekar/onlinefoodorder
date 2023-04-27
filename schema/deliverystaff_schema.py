from pydantic import BaseModel,validator,ValidationError
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    mobile_no: str
    created_at:datetime
    updated_at:datetime