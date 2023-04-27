from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Users1(db_config.BASE):
    __tablename__ = 'users1'
    Id = Column(Integer,autoincrement=True,primary_key=True)
    email= Column(String,unique=True,default = None)
    password = Column(String,default = None)
    
    


