from pydantic import BaseModel,validator,ValidationError
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

# Define user model
class UserCreate(BaseModel):
    email: str
    password: str