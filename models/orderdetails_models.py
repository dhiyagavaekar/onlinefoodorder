from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Orderdetails2(db_config.BASE):
    __tablename__ = 'orderdetails2'
    orderdetailId = Column(Integer,autoincrement=True,primary_key=True)
    orderId = Column(String,ForeignKey("order1.orderId"))
    deliveryId= Column(String,ForeignKey("delivery.deliveryId"))
    orderdate= Column(DateTime,default = None)
    status =  Column(String,default = None)
    created_at=Column(DateTime, default=None)
    updated_at=Column(DateTime, default=None)