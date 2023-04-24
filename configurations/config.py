from pydantic import BaseSettings

class Settings(BaseSettings):
    LOG_LEVEL='DEBUG'
    SERVER='3.108.193.79'
    UID='DBUser'
    PASSWORD='CStore@db123'
    DATABASE='CStoreiQDB'
    PORT='1433'
 