from pydantic import BaseModel,validator,ValidationError
from datetime import datetime
from typing import Optional
from enum import Enum
class Role(str,Enum):
    customers ="customers"
    deliverystaff = "deliverystaff"
    restaurent = "restaurent"