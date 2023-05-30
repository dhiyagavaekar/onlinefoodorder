from models import customers_models,order_models,foodItems_models,orderdetails_models
from configurations import config
from fastapi import HTTPException
from . import helper as customer_helper
from fastapi import Depends, HTTPException

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
    
# @app.put("/items/{item_id}")
def softdelete_order(id, session):
    order=session.query(order_models.Order1).filter(
        order_models.Order1.orderId==id
        ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Item not found")
    order.deleted = True
    session.commit()
    return {"message": "Item soft-deleted"}


def get_customer_details(username,password,db):
   
    customer = db.query(customers_models.Customers).filter(customers_models.Customers.email==username,\
        customers_models.Customers.password==password).first() 
    
    if customer is None:
             raise HTTPException(status_code=401, detail="Unable to verify credentials")
    
    customerId = customer.customerId
    customers =\
        db.query(
            customers_models.Customers
        ).filter(customers_models.Customers.customerId==customerId).all()
    
    return customers




   




