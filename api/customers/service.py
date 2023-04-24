from models import customers_models,order_models,bills_models,foodItems_models,orderdetails_models,\
    restaurent_models
from configurations import config
from fastapi import HTTPException,Response
from common import helper as common_helper
from . import helper as customer_helper

settings=config.Settings()

def read_customers(session):

    # get the users data with the given id
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

def getorderdetailbyid(customerid,orderid,restaurentid,session):#1,1,1

    # get the users data with the given id
    customers =\
        session.query(
            order_models.Order1
        ).filter(order_models.Order1.customerId==customerid,order_models.Order1.restaurentId==restaurentid).all()
    if not customers:
        raise HTTPException(
            status_code=404, detail=f"users data with id {id} not found"
        )
    else:
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

def orderupdate(id: int,customerid:int, orderupdate, session):
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
    # check if store_location_fee data with given id exists. If not, raise exception and return 404 not found response
    if not order:
        raise HTTPException(
            status_code=404, detail=f"store_location_fee data with id {id} not found"
        )

    return order

def createorder(id,order,session):  
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


def delete_order(id, session):
        order=session.query(order_models.Order1).filter(
        order_models.Order1.orderId==id
        ).delete() 
        print(order)
        
        session.commit()
        
        return True
   




