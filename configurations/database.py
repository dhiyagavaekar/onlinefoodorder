# from sqlalchemy import create_engine ,MetaData
# from .config import Settings
# from sqlalchemy.engine import URL
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# settings=Settings()
# connection_string = 'DRIVER={SQL Server}=SERVER'+settings.SERVER+';PORT='+settings.PORT+';DATABASE='+settings.DATABASE+';UID='+settings.UID+';PWD='+settings.PASSWORD

# connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

# print(connection_url)
# # Create a sqlite engine instance
# ENGINE = create_engine(connection_url)
# metadata = MetaData(ENGINE)

# # Create a DeclarativeMeta instance
# BASE = declarative_base()

# # Create SessionLocal class from sessionmaker factory
# SESSION_LOCAL = sessionmaker(bind=ENGINE, expire_on_commit=False)

from .config import Settings
from sqlalchemy import create_engine,Table,MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
settings=Settings()
try:
    #connection_string = 'DRIVER={SQL Server};SERVER='+settings.SERVER+';PORT='+settings.PORT+';DATABASE='+settings.DATABASE+';UID='+settings.UID+';PWD='+settings.PASSWORD
    # connection_string = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+settings.SERVER+';PORT='+settings.PORT+';DATABASE='+settings.DATABASE+';UID='+settings.UID+';PWD='+settings.PASSWORD
    connection_string = "mysql+mysqlconnector://root@localhost/onlineFoodOrder"
    ENGINE = create_engine(connection_string)
    # connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

    # ENGINE = create_engine(connection_url, connect_args = {
    #     "TrustServerCertificate": "yes"
    # },)

    metadata = MetaData(ENGINE)

    BASE = declarative_base()


    SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
except Exception as e:
    print(e)