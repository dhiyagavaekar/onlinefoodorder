from sqlalchemy import *
from configurations import database as db_config
from datetime import datetime

# Define Department class inheriting from Base
class Bills1(db_config.BASE):
    __tablename__ = 'bills1'
    billId = Column(Integer, primary_key=True, autoincrement=True)
    orderId = Column(Integer,ForeignKey("order1.orderId"))
    deliverycharges = Column(Integer, default=None)
    created_at=Column(DateTime, default=None)
    updated_at=Column(DateTime, default=None)
    
