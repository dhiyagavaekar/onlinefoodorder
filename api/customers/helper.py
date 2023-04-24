def transform_json_data_into_order_model(
    order_model, order_json):
    # order_model.customerId=order_json['customerId']
    order_model.restaurentId=order_json['restaurentId']
    order_model.foodItemId=order_json['foodItemId']
    order_model.quantity=order_json['quantity']
    order_model.instructions=order_json['instructions']
    order_model.created_at=order_json['created_at']
    order_model.updated_at=order_json['updated_at']
    

    return order_model

def transform_json_data_into_order1_model(
    order_model, order_json):
    order_model.customerId=order_json['customerId']
    order_model.restaurentId=order_json['restaurentId']
    order_model.foodItemId=order_json['foodItemId']
    order_model.quantity=order_json['quantity']
    order_model.instructions=order_json['instructions']
    order_model.created_at=order_json['created_at']
    order_model.updated_at=order_json['updated_at']
    

    return order_model