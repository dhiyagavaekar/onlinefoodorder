from pydantic import BaseModel,validator,ValidationError
from datetime import datetime
from typing import Optional,List
from configurations import database as config_db
# Create Item Schema (Pydantic Model)

class FooditemCreate(BaseModel):
    # restaurentId :Optional[int] = None
    name: Optional[str] = None
    category:Optional[str] = None
    price:Optional[int] = None
    description:Optional[str] = None
    # created_at:Optional[datetime] = None
    # updated_at:Optional[datetime] = None
    
class FooditemUpdate(BaseModel):
    
    # restaurentId :Optional[int] = None
    name: Optional[str] = None
    category:Optional[str] = None
    price:Optional[int] = None
    description:Optional[str] = None
    # created_at:Optional[datetime] = None
    # updated_at:Optional[datetime] = None
    
class Fooditem(BaseModel):
    foodItemId: Optional[int] = None
    restaurentId: Optional[int] = None
    name: Optional[str] = None
    category:Optional[str] = None
    price:Optional[int] = None
    description:Optional[str] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
    

    
    class Config:
        orm_mode = True