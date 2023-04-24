from configurations import database as db_config
from configurations import config
import pyodbc
settings=config.Settings()
def get_session():
    session = db_config.SESSION_LOCAL()
    try:
        yield session
    finally:
        session.close()

def raw_connection():
        #conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+settings.SERVER+';PORT='+settings.PORT+';DATABASE='+settings.DATABASE+';UID='+settings.UID+';PWD='+settings.PASSWORD, autocommit=True)
        server = 'localhost'

        conn = pyodbc.connect(
        'Driver={ODBC Driver 18 for SQL Server};'
        'SERVER='+settings.SERVER+';'
        'DATABASE='+settings.DATABASE+';'
        'PORT='+settings.PORT+';'
        'UID='+settings.UID+';'
        'PWD='+settings.PASSWORD+';'
        'TrustServerCertificate=yes;'
        )
        
        return conn.cursor()


def filterEmptyValue(params:list):
    function_params=''
    for x in  params:
        if x == None or x == "":
            function_params+="'{}',".format('NULL')
        elif type(x)==str:
            if x!=params[len(params)-1]:
                function_params+="'{}',".format(x)
            else:
                function_params+="'{}'".format(x)
        else:
            if x!=params[len(params)-1]:
                function_params+="{},".format(str(x))
            else:
                function_params+="{}".format(str(x))
    return function_params


