from sqlalchemy import *
from configurations import database as db_config

# Define Department class inheriting from Base
class Users(db_config.BASE):
    __tablename__ = 'users'
    Id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String,default = None)
    email= Column(String,unique=True,default = None)
    password = Column(String,default = None)
    
    
