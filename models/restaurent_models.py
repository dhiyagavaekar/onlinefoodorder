from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Restaurent(db_config.BASE):
    __tablename__ = 'restaurent'
    restaurentId = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String,default = None)
    address = Column(String,default = None)
    city= Column(String,default = None)
    state= Column(String,default = None)
    mobile_no= Column(String,default = None)
    created_at=Column(DateTime, default=None)
    updated_at=Column(DateTime, default=None)

