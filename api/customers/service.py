from models import customers_models,order_models,foodItems_models,orderdetails_models
from configurations import config
from fastapi import HTTPException,Response
from . import helper as customer_helper
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

settings=config.Settings()

def read_customers(session):

    # get the users data 
    customers =\
        session.query(
            customers_models.Customers
        ).all()

    # check if users data with given id exists. If not, raise exception and return 404 not found response
    if not customers:
        raise HTTPException(
            status_code=404, detail=f"users data with id {id} not found"
        )

    return customers

def getOrderDetailbyId(orderid,session):#1,1,1
#customers can see their order details
    order_details = session.query(order_models.Order1,foodItems_models.FoodItems,\
            orderdetails_models.Orderdetails2).\
            join(foodItems_models.FoodItems,order_models.Order1.foodItemId==foodItems_models.FoodItems.foodItemId).\
            filter(order_models.Order1.orderId==orderid).\
            with_entities(order_models.Order1.orderId,order_models.Order1.restaurentId,order_models.Order1.customerId,\
                order_models.Order1.quantity,order_models.Order1.instructions,foodItems_models.FoodItems.name,\
                foodItems_models.FoodItems.price).\
            all()
    
    for order in order_details:
        output={
            "customerId":order.customerId,
            "restaurentId":order.restaurentId,
            "orderId":order.orderId,
            "fooditem":{
                "name":order.name,
                "quantity":order.quantity,
                "price":order.price
            }
        }    

    return output

def orderUpdate(id: int,customerid:int, orderupdate, session):
    orderupdate_json_data = dict(orderupdate)
#         {
#   "orderId": 1,
#   "restaurentId": 1,
#   "foodItemId": 1,
#   "quantity": 3,
#   "instructions": "heavy cheese",
#   "created_at": "2023-04-20T12:13:29",
#   "updated_at": "2023-04-20T12:13:29"
# }
 #customer can update their order 
    order = session.query(order_models.Order1).filter(
        order_models.Order1.orderId== id,order_models.Order1.customerId==customerid
        ).first()
    
    
    if order:  
        order =\
                    customer_helper.transform_json_data_into_order_model(
                        order, 
                        orderupdate_json_data
                    )
        session.commit()
    # check if order data with given id exists. If not, raise exception and return 404 not found response
    if not order:
        raise HTTPException(
            status_code=404, detail=f"store_location_fee data with id {id} not found"
        )

    return order

def createOrder(id,order,session):  
    # customer can insert their order
    customer = session.query(order_models.Order1).filter(
       order_models.Order1.customerId==id
        ).first() 
    if not customer:
        raise HTTPException(
            status_code=404, detail=f"customer with id {id} not found"
        )
        #         {
        #   "orderId": 12,
        #   "restaurentId": 1,
        #   "foodItemId": 2,
        #   "quantity": 2,
        #   "instructions": "yes",
        #   "created_at": "2023-04-21T11:20:27",
        #   "updated_at": "2023-04-21T11:20:27"
        # }
        
    else:
        order =\
            customer_helper.transform_json_data_into_order1_model(
                order_models.Order1(), 
                dict(order)
            )
        # add it to the session and commit it
        session.add(order)
        session.commit()
        session.refresh(order)

        # return the order object
    return order   

# customer can delete the order
def deleteOrder(id, session):
        order=session.query(order_models.Order1).filter(
        order_models.Order1.orderId==id
        ).delete() 
        print(order)
        
        session.commit()
        
        return True
    
SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(customers_models.Customers).filter(customers_models.Customers.email == email).all()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# @login_routes1.post("/signup1", response_model=userlogin1_schema.Token)
def signup(user, db):
    db_user = db.query(customers_models.Customers).filter(customers_models.Customers.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = customers_models.Customers(email=user.email, password=hashed_password,firstname=user.firstname,\
        lastname=user.lastname,address=user.address,city=user.city,state=user.state,mobile_no=user.mobile_no,created_at=user.created_at,updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# @login_routes1.post("/login1", response_model=userlogin1_schema.Token)
def login(form_data, db):
    user = db.query(customers_models.Customers).filter(customers_models.Customers.email == form_data.username).first()
    print
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    data = {
        "sub": user.email,
        "customerId": user.customerId,
        "firstname": user.firstname,
        "email":user.email
        
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}

def create_token(form_data, db):
    # user = authenticate_user(db, form_data.username, form_data.password)
    user = db.query(customers_models.Customers).filter(customers_models.Customers.email == form_data.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        
        "customerId": user.customerId,
        "firstname": user.firstname,
        "lastname":user.lastname,
        "email": user.email,
        "mobile_no.":user.mobile_no
        
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"CustomerData":access_token_data,"access_token": access_token}

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         customerId:str=payload.get("customerId")
#         firstname: str = payload.get("firstname")
#         if id is None or firstname is None or email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         token_data= {"email": email, "customerId":customerId,"firstname": firstname}
#         return token_data
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid authentication token")




   




