from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class FoodOrder(db_config.BASE):
    __tablename__ = 'foodorder'
    Id = Column(Integer,autoincrement=True,primary_key=True)
    orderId= Column(String,ForeignKey("order1.orderId"))
    foodItemId = Column(String,ForeignKey("foodItems.foodItemId"))
    quantity= Column(String,default = None)