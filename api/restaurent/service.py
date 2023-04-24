from models import customers_models,order_models,bills_models,foodItems_models,orderdetails_models,\
    restaurent_models
from configurations import config
from fastapi import HTTPException,Response
from common import helper as common_helper
from . import helper as customer_helper

settings=config.Settings()



def getallrestaurents(session):

    # get the users data with the given id
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

def addfooditem(id,addfood,session):  
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
        
def fooditemupdate(fooditemid: int,restaurentid:int, fooditemupdate, session):
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

def delete_fooditem(restaurentid, fooditemid,session):
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