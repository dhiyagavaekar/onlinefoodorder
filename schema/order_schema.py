from pydantic import BaseModel,validator,ValidationError
from datetime import datetime
from typing import Optional,List
from configurations import database as config_db
# Create Item Schema (Pydantic Model)

class OrderCreate(BaseModel):
    customerId: int 
    restaurentId: int
    foodItemId: Optional[int] = None
    quantity:Optional[int] = None
    instructions:Optional[str] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
    
class OrderUpdate(BaseModel):
    
    #customerId: int 
    restaurentId: int
    foodItemId: Optional[int] = None
    quantity:Optional[int] = None
    instructions:Optional[str] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
    
class Order(BaseModel):
    orderId: Optional[int] = None
    #customerId: int 
    restaurentId:int
    foodItemId: Optional[int] = None
    quantity:Optional[int] = None
    instructions:Optional[str] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
    

    
    class Config:
        orm_mode = True