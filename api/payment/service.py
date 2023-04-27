from models import customers_models,order_models,bills_models,foodItems_models,foodorder_models,\
    payment_models
from configurations import config
from fastapi import HTTPException,Response
from common import helper as common_helper
#from . import helper as customer_helper

settings=config.Settings()



def get_paytment_of_order(session):

    # get the users data with the given id
    payment =\
        session.query(payment_models.Payment,bills_models.Bills1).\
            join(bills_models.Bills1,payment_models.Payment.billId==bills_models.Bills1.billId).\
            with_entities(bills_models.Bills1.orderId,bills_models.Bills1.deliverycharges,\
            payment_models.Payment.customerId,payment_models.Payment.paymenttype,payment_models.Payment.paymentdate).all()

    # check if users data with given id exists. If not, raise exception and return 404 not found response
    if not payment:
        raise HTTPException(
            status_code=404, detail=f"order data not found"
        )

    return payment

def totalPayment(orderid,session):

    # get the users data with the given id
    orderpayment =\
        session.query(foodorder_models.FoodOrder,foodItems_models.FoodItems).\
            join(foodItems_models.FoodItems,foodorder_models.FoodOrder.foodItemId==foodItems_models.FoodItems.foodItemId).\
            filter(foodorder_models.FoodOrder.orderId==orderid).\
            with_entities(foodorder_models.FoodOrder.orderId,foodorder_models.FoodOrder.foodItemId,foodorder_models.FoodOrder.quantity
            ,foodItems_models.FoodItems.price,foodItems_models.FoodItems.name).all()
    output=[]
    output1 = []
    for payment in orderpayment:
        total = payment.quantity*payment.price
        
        output.append(
            total)
        output1.append({
            "orderId":payment.orderId,
            "foodItemId":payment.foodItemId,
            "foodname":payment.name,
            "quantity":payment.quantity,
            "price":payment.price,
            "total-price":total
            
        })
    
    s=sum(output)
    result = {"order":output1,"total amount":s}  
    return result