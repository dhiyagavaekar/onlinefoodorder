from models import customers_models,order_models,bills_models,foodItems_models,orderdetails_models,\
    restaurent_models,foodorder_models,delivery_models,deliverystaff_models
from configurations import config
from fastapi import HTTPException,Response
from common import helper as common_helper


settings=config.Settings()

def read_deliverydetails(restaurentid,session):#2

    # get the users data with the given id
    restaurent =session.query(order_models.Order1).filter(order_models.Order1.restaurentId==restaurentid).all()
    
    if restaurent:
        customers =session.query(order_models.Order1,customers_models.Customers).\
            join(customers_models.Customers,order_models.Order1.customerId==customers_models.Customers.customerId).\
            join(orderdetails_models.Orderdetails2,order_models.Order1.orderId==orderdetails_models.Orderdetails2.orderId).\
            join(delivery_models.Delivery,orderdetails_models.Orderdetails2.deliveryId==delivery_models.Delivery.deliveryId).\
            join(deliverystaff_models.Deliverystaff,delivery_models.Delivery.deliverystaffId==deliverystaff_models.Deliverystaff.deliverystaffId).\
            filter(order_models.Order1.restaurentId==restaurentid).\
            with_entities(order_models.Order1.orderId,order_models.Order1.customerId,order_models.Order1.restaurentId,customers_models.Customers.firstname,\
                customers_models.Customers.lastname,customers_models.Customers.address,customers_models.Customers.mobile_no,\
                delivery_models.Delivery.deliverystaffId,deliverystaff_models.Deliverystaff.firstname.label('name'),\
                deliverystaff_models.Deliverystaff.mobile_no.label('dmob')   ).all()
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

def get_deliveryofstatus(status,session):#2

    # get the users data with the given id
    status =session.query(orderdetails_models.Orderdetails2).\
        filter(orderdetails_models.Orderdetails2.status==status).\
        with_entities(orderdetails_models.Orderdetails2.orderId,orderdetails_models.Orderdetails2.orderdate,\
            orderdetails_models.Orderdetails2.deliveryId,orderdetails_models.Orderdetails2.created_at,orderdetails_models.Orderdetails2.updated_at).all()
    
    return status

def get_deliveryofallstatus(session):#2

    # get the users data with the given id
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
    
    