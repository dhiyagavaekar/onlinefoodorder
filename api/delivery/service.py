from models import customers_models,order_models,bills_models,foodItems_models,orderdetails_models,\
    restaurent_models,foodorder_models,delivery_models,deliverystaff_models
from configurations import config
from fastapi import HTTPException,Response

from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

settings=config.Settings()

def readCustomerDeliveryDetails(restaurentid,session):#2

    # restaurent can get their differentorder details details

    customers =session.query(order_models.Order1,customers_models.Customers).\
            join(customers_models.Customers,order_models.Order1.customerId==customers_models.Customers.customerId).\
            join(orderdetails_models.Orderdetails2,order_models.Order1.orderId==orderdetails_models.Orderdetails2.orderId).\
            join(delivery_models.Delivery,orderdetails_models.Orderdetails2.deliveryId==delivery_models.Delivery.deliveryId).\
            join(deliverystaff_models.Deliverystaff,delivery_models.Delivery.deliverystaffId==deliverystaff_models.Deliverystaff.deliverystaffId).\
            filter(order_models.Order1.restaurentId==restaurentid).\
            with_entities(order_models.Order1.orderId,order_models.Order1.customerId,order_models.Order1.restaurentId,customers_models.Customers.firstname,\
                customers_models.Customers.lastname,customers_models.Customers.address,customers_models.Customers.mobile_no,\
                delivery_models.Delivery.deliverystaffId,deliverystaff_models.Deliverystaff.firstname.label('name'),\
                deliverystaff_models.Deliverystaff.mobile_no.label('dmob')).all()
    output = []
    for customer in customers:
        output.append({
            "orderId":customer.orderId,
            "customerId":customer.customerId,
            "name":customer.firstname +" "+ customer.lastname,
            "address":customer.address,
            "mobile_no":customer.mobile_no,
            "delivery_details":
                {
            "deliverystaffId":customer.deliverystaffId,
            "deliveryname":customer.name,
            "mobile_no.":customer.dmob}
        })
        
    return output

def getDeliveryDetailsByOrderId(orderid,session):
    orderdetails = session.query(orderdetails_models.Orderdetails2).\
        join(delivery_models.Delivery,orderdetails_models.Orderdetails2.deliveryId==delivery_models.Delivery.deliveryId).\
        join(deliverystaff_models.Deliverystaff,delivery_models.Delivery.deliverystaffId==deliverystaff_models.Deliverystaff.deliverystaffId).\
        filter(orderdetails_models.Orderdetails2.orderId==orderid).\
        with_entities(orderdetails_models.Orderdetails2.orderId,deliverystaff_models.Deliverystaff.firstname,\
                deliverystaff_models.Deliverystaff.lastname,deliverystaff_models.Deliverystaff.mobile_no,delivery_models.Delivery.instructions,\
                    delivery_models.Delivery.deliverytime).all()
        
    for detail in orderdetails:
        output=({
            "orderId":detail.orderId,
            "delivery_staff_details":
                {
            "name":detail.firstname +detail.lastname,
            "mobile_no.":detail.mobile_no,
            "instructions":detail.instructions,
            "deliverytime":detail.deliverytime
            }
        })
        
    return output

        

def getDeliveryofSpecificStatus(status,session):#2

    # restaurent can getorder details of specific status
    status =session.query(orderdetails_models.Orderdetails2).\
        filter(orderdetails_models.Orderdetails2.status==status).\
        with_entities(orderdetails_models.Orderdetails2.orderId,orderdetails_models.Orderdetails2.orderdate,\
            orderdetails_models.Orderdetails2.deliveryId,orderdetails_models.Orderdetails2.created_at,orderdetails_models.Orderdetails2.updated_at).all()
    
    return status

def getDeliveryofAllStatus(session):#2

    # restaurent get order details of all status
    status =session.query(orderdetails_models.Orderdetails2).\
        with_entities(orderdetails_models.Orderdetails2.orderId,orderdetails_models.Orderdetails2.orderdate,orderdetails_models.Orderdetails2.status,\
            orderdetails_models.Orderdetails2.deliveryId,orderdetails_models.Orderdetails2.created_at,orderdetails_models.Orderdetails2.updated_at).all()
    
    groups = {}
    for ele in status:
            status = ele.status
            if status not in groups:
                groups[status] = []
            groups[status].append({
                'orderId': ele.orderId,
                'orderdate': ele.orderdate,
                'deliveryId': ele.deliveryId,
                'created_at': ele.created_at,
                'updated_at':ele.updated_at
            })
        

        # Convert the groups to the desired output format
    output = []
    for status, data in groups.items():
            output.append({
                'key': status,
                'data': data,
            })
        
    return output

#startlogin
SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# # @login_routes1.post("/signup1", response_model=userlogin1_schema.Token)
def deliverystaff_signup(user, db):
    db_user = db.query(deliverystaff_models.Deliverystaff).filter(deliverystaff_models.Deliverystaff.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = deliverystaff_models.Deliverystaff(email=user.email, password=hashed_password,firstname=user.firstname,\
        lastname=user.lastname,mobile_no=user.mobile_no,created_at=user.created_at,updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# # @login_routes1.post("/login1", response_model=userlogin1_schema.Token)
def deliverystaff_login(form_data, db):
    user = db.query(deliverystaff_models.Deliverystaff).filter(deliverystaff_models.Deliverystaff.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    data = {
        "sub": user.email,
        "deliverystaffId": user.deliverystaffId,
        "firstname": user.firstname,
        "email":user.email
        
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}

def create_token(form_data, db):
    # user = authenticate_user(db, form_data.username, form_data.password)
    user = db.query(deliverystaff_models.Deliverystaff).filter(deliverystaff_models.Deliverystaff.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        
        "deliverystaffId": user.deliverystaffId,
        "firstname": user.firstname,
        "lastname":user.lastname,
        "email": user.email,
        "mobile_no.":user.mobile_no
        
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"CustomerData":access_token_data,"access_token": access_token}
    