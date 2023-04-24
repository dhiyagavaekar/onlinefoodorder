from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Customers(db_config.BASE):
    __tablename__ = 'customers'
    customerId = Column(Integer,autoincrement=True,primary_key=True)
    firstname = Column(String,default = None)
    lastname= Column(String,default = None)
    address = Column(String,default = None)
    city= Column(String,default = None)
    state= Column(String,default = None)
    mobile_no= Column(String,default = None)
    created_at=Column(DateTime, default=None)
    updated_at=Column(DateTime, default=None)
    
