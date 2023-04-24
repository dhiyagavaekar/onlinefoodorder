from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class FoodItems(db_config.BASE):
    __tablename__ = 'foodItems'
    foodItemId = Column(Integer,autoincrement=True,primary_key=True)
    restaurentId = Column(String,ForeignKey("restaurent.restaurentId"))
    name = Column(String,default = None)
    category= Column(String,default = None)
    price= Column(Integer,default = None)
    description= Column(String,default = None)
    created_at=Column(DateTime, default=None)
    updated_at=Column(DateTime, default=None)
