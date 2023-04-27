from models import customers_models,order_models,bills_models,foodItems_models,orderdetails_models,\
    restaurent_models,foodorder_models
from configurations import config
from fastapi import HTTPException,Response
from common import helper as common_helper
from . import helper as customer_helper

settings=config.Settings()

def read_orders(session):

    # get all orders details
    order =\
        session.query(
            order_models.Order1
        ).all()

    # check if users data with given id exists. If not, raise exception and return 404 not found response
    if not order:
        raise HTTPException(
            status_code=404, detail=f"order data not found"
        )

    return order

# restaurent will get order details by orderid
def read_OrderbyId(orderid,session):#1,2
    order =\
        session.query(order_models.Order1,foodorder_models.FoodOrder,foodItems_models.FoodItems)\
        .join(foodorder_models.FoodOrder,order_models.Order1.orderId==foodorder_models.FoodOrder.orderId)\
        .join(foodItems_models.FoodItems,foodorder_models.FoodOrder.foodItemId==foodItems_models.FoodItems.foodItemId)\
        .filter(order_models.Order1.orderId==orderid)\
        .with_entities(order_models.Order1.orderId,order_models.Order1.customerId,order_models.Order1.restaurentId,\
            order_models.Order1.instructions,foodorder_models.FoodOrder.foodItemId,foodorder_models.FoodOrder.quantity,\
                foodItems_models.FoodItems.name,foodItems_models.FoodItems.price).all()
    output = []
    for orders in order:
        
        role=orders.foodItemId
        quantity = orders.quantity
        name = orders.name
        price=orders.price

        output.append({  
                       "fooditemid":role,
                       "quantity":quantity,
                       "name":name,
                       "price":price})
        fooddetails={"orderId": orders.orderId,
                    "customerId": orders.customerId,
                    "restaurentId":orders.restaurentId,
                    "instructions":orders.instructions,
                    "fooditems":output
                    }
        
    return fooddetails
    