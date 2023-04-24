from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Payment(db_config.BASE):
    __tablename__ = 'payment'
    paymentId = Column(Integer,autoincrement=True,primary_key=True)
    billId = Column(String,ForeignKey("bills.billId"))
    customerId = Column(String,ForeignKey("customers.customerId"))
    paymenttype= Column(String,default = None)
    paymentdate= Column(DateTime,default = None)
    status =  Column(String,default = None)
    created_at=Column(DateTime, default=None)
    updated_at=Column(DateTime, default=None)