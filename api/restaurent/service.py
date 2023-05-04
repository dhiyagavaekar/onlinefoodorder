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
from api.registration_login import service as reg_service
from fastapi.encoders import jsonable_encoder


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
# def addFoodItem(id,addfood,session):  
#     restaurent = session.query(foodItems_models.FoodItems).filter(
#        foodItems_models.FoodItems.restaurentId==id
#         ).first() 
#     if not restaurent:
#         raise HTTPException(
#             status_code=404, detail=f"customer with id {id} not found"
#         )
        
#     else:
#         addfood =\
#             customer_helper.transform_json_data_into_addfood_model(
#                 foodItems_models.FoodItems(), 
#                 dict(addfood)
#             )
#         # add it to the session and commit it
#         session.add(addfood)
#         session.commit()
#         session.refresh(addfood)

#         # return the addfood object
#     return addfood  
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

# Restaurent can addfooditems
def addFoodItem(addfood,session,username):  
    
    restaurent = session.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email==username).first()  
    if restaurent is None:
             raise HTTPException(status_code=401, detail="Unable to verify credentials")
    
    restaurentId = restaurent.restaurentId
    created_at=datetime.now().date()
    updated_at=datetime.now().date()
    foodItem = foodItems_models.FoodItems(**addfood.dict(),created_at=created_at,updated_at=updated_at,restaurentId=restaurentId) 
    
    session.add(foodItem)
    session.commit()
    session.refresh(foodItem)

        # return the addfood object
    return foodItem  

# restaurent can update their food items        
# def foodItemUpdate(fooditemid: int,restaurentid:int, fooditemupdate, session):
#     fooditemupdate_json_data = dict(fooditemupdate)

    
#     fooditem = session.query(foodItems_models.FoodItems).filter(
#         foodItems_models.FoodItems.foodItemId== fooditemid,foodItems_models.FoodItems.restaurentId==restaurentid
#         ).first()
    
    
#     if  fooditem:  
#         fooditem =\
#                     customer_helper.transform_json_data_into_updatefood_model(
#                        fooditem, 
#                         fooditemupdate_json_data
#                     )
#         session.commit()
#     # check if store_location_fee data with given id exists. If not, raise exception and return 404 not found response
#     if not  fooditem:
#         raise HTTPException(
#             status_code=404, detail=f"store_location_fee data with id {id} not found"
#         )

#     return  fooditem
#         # {
        #   "foodItemId": 7,
        #   "restaurentId": 2,
        #   "name": "plain rice",
        #   "category": "dinner",
        #   "price": 100,
        #   "description": "low spicy",
        #   "created_at": "2023-04-21T11:57:16",
        #   "updated_at": "2023-04-21T11:57:16"
        # }

def foodItemUpdate(id,order_update,session,username):
    
    restaurent = session.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email==username).first()  
    if restaurent is None:
             raise HTTPException(status_code=401, detail="Unable to verify credentials")
    
    existing_item=session.query(foodItems_models.FoodItems).filter(
        foodItems_models.FoodItems.foodItemId==id)
    if not existing_item.first():
        return {"message":f"No details exist for item id {id}"}
    if existing_item.first().restaurentId==restaurent.restaurentId:
        existing_item.update(jsonable_encoder(order_update))
        session.commit()
        return {"message":f"Item successfully updated"}
    else:
        return f"you are not authorised"
    

# def delete_foodItem(restaurentid, fooditemid,session):
#     restaurent = session.query(foodItems_models.FoodItems).filter(
#        foodItems_models.FoodItems.restaurentId==restaurentid
#         ).all()
#     if restaurent:
#         fooditem=session.query(foodItems_models.FoodItems).filter(
#         foodItems_models.FoodItems.foodItemId==fooditemid
#         ).delete() 
#         print(fooditem)
        
#         session.commit()
        
#         return f"fooditem deleted"

#restaurent can delete food items

def delete_foodItem(id,session,username):
    restaurent = session.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email==username).first()  
    if restaurent is None:
             raise HTTPException(status_code=401, detail="Unable to verify credentials")
    
    existing_item=session.query(foodItems_models.FoodItems).filter(
        foodItems_models.FoodItems.foodItemId==id)
    if not existing_item.first():
        return {"message":f"No details exist for item id {id}"}
    if existing_item.first().restaurentId==restaurent.restaurentId:
        existing_item.delete()    
        session.commit()    
        return f"fooditem deleted"
    else:
        return f"you are not authorised"
    
def get_restaurent_details(username,password,db):
    
    restaurent = db.query(restaurent_models.Restaurent).filter(restaurent_models.Restaurent.email==username,\
        restaurent_models.Restaurent.password==password).first()  
    if restaurent is None:
             raise HTTPException(status_code=401, detail="Unable to verify credentials")
    
 
    restaurentId = restaurent.restaurentId
    restaurent =\
        db.query(
            restaurent_models.Restaurent
        ).filter(restaurent_models.Restaurent.restaurentId==restaurentId).all()
    
    return restaurent


    
