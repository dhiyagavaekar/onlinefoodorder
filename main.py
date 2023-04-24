import routes

from fastapi import FastAPI,Request
from configurations import base as base_config
from configurations import config
import pyodbc
from utils.conversion_util import convert_pagination_sql
import os
from fastapi.middleware.cors import CORSMiddleware
path=os.path.dirname(os.path.abspath(__file__))
base_config.initialize_db_if_not_created()
# Initialize app
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for routes in routes.routes_path:
    app.include_router(routes)