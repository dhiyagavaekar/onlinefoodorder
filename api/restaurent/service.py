from . import helper as customer_helper
from models import customers_models,order_models,bills_models,foodItems_models,orderdetails_models,\
    restaurent_models,foodorder_models,delivery_models,deliverystaff_models
from configurations import config
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

settings=config.Settings()



def getAllRestaurents(session):

    # get all restaurent data
    restaurent =\
        session.query(
            restaurent_models.Restaurent
        ).all()

    # check if users data with given id exists. If not, raise exception and return 404 not found response
    if not restaurent:
        raise HTTPException(
            status_code=404, detail=f"order data not found"
        )

    return restaurent

# Restaurent can addfooditems
def addFoodItem(id,addfood,session):  
    restaurent = session.query(foodItems_models.FoodItems).filter(
       foodItems_models.FoodItems.restaurentId==id
        ).first() 
    if not restaurent:
        raise HTTPException(
            status_code=404, detail=f"customer with id {id} not found"
        )
        
    else:
        addfood =\
            customer_helper.transform_json_data_into_addfood_model(
                foodItems_models.FoodItems(), 
                dict(addfood)
            )
        # add it to the session and commit it
        session.add(addfood)
        session.commit()
        session.refresh(addfood)

        # return the addfood object
    return addfood  
        # {
        #   "foodItemId": 7,
        #   "restaurentId": 2,
        #   "name": "plain rice",
        #   "category": "dinner",
        #   "price": 60,
        #   "description": "made with rice",
        #   "created_at": "2023-04-21T11:46:08",
        #   "updated_at": "2023-04-21T11:46:08"
        # }

# restaurent can update their food items        
def foodItemUpdate(fooditemid: int,restaurentid:int, fooditemupdate, session):
    fooditemupdate_json_data = dict(fooditemupdate)

    
    fooditem = session.query(foodItems_models.FoodItems).filter(
        foodItems_models.FoodItems.foodItemId== fooditemid,foodItems_models.FoodItems.restaurentId==restaurentid
        ).first()
    
    
    if  fooditem:  
        fooditem =\
                    customer_helper.transform_json_data_into_updatefood_model(
                       fooditem, 
                        fooditemupdate_json_data
                    )
        session.commit()
    # check if store_location_fee data with given id exists. If not, raise exception and return 404 not found response
    if not  fooditem:
        raise HTTPException(
            status_code=404, detail=f"store_location_fee data with id {id} not found"
        )

    return  fooditem
        # {
        #   "foodItemId": 7,
        #   "restaurentId": 2,
        #   "name": "plain rice",
        #   "category": "dinner",
        #   "price": 100,
        #   "description": "low spicy",
        #   "created_at": "2023-04-21T11:57:16",
        #   "updated_at": "2023-04-21T11:57:16"
        # }

#restaurent can delete food items
def delete_foodItem(restaurentid, fooditemid,session):
    restaurent = session.query(foodItems_models.FoodItems).filter(
       foodItems_models.FoodItems.restaurentId==restaurentid
        ).all()
    if restaurent:
        fooditem=session.query(foodItems_models.FoodItems).filter(
        foodItems_models.FoodItems.foodItemId==fooditemid
        ).delete() 
        print(fooditem)
        
        session.commit()
        
        return f"fooditem deleted"
    
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
def signup(user, db):
    db_user = db.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = restaurent_models.Restaurent(email=user.email, password=hashed_password,name=user.name,\
        address=user.address,city=user.city,state=user.state,mobile_no=user.mobile_no,created_at=user.created_at,updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# # @login_routes1.post("/login1", response_model=userlogin1_schema.Token)
def login(form_data, db):
    user = db.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    data = {
        "sub": user.email,
        "restaurentId": user.restaurentId,
        "name": user.name,
        "email":user.email
        
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}

def create_token(form_data, db):
    # user = authenticate_user(db, form_data.username, form_data.password)
    user = db.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        
        "restaurentId": user.restaurentId,
        "name": user.name,
        "email": user.email,
        "mobile_no.":user.mobile_no
        
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"CustomerData":access_token_data,"access_token": access_token}