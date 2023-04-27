from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Order1(db_config.BASE):
    __tablename__ = 'order1'
    orderId = Column(Integer,autoincrement=True,primary_key=True)
    customerId = Column(String,ForeignKey("customers.customerId"))
    restaurentId = Column(String,ForeignKey("restaurent.restaurentId"))
    foodItemId = Column(String,ForeignKey("foodItems.foodItemId"))
    quantity= Column(String,default = None)
    instructions= Column(String,default = None)
    created_at=Column(DateTime, default=None)
    updated_at=Column(DateTime, default=None)
    
    # deleted = Column(Boolean, default=False)