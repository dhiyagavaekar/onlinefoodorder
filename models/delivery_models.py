from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Delivery(db_config.BASE):
    __tablename__ = 'delivery'
    deliveryId = Column(Integer,autoincrement=True,primary_key=True)
    deliverystaffId = Column(String,ForeignKey("deliverystaff.deliverystaffId"))
    address = Column(String,default = None)
    instructions= Column(String,default = None)
    status= Column(String,default = None)
    deliverytime= Column(DateTime,default = None)
    # created_at=Column(DateTime, default=None)
    # updated_at=Column(DateTime, default=None)
