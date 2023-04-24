def transform_json_data_into_addfood_model(
    food_model, food_json):
    food_model.restaurentId=food_json['restaurentId']
    food_model.name=food_json['name']
    food_model.category=food_json['category']
    food_model.price=food_json['price']
    food_model.description=food_json['description']
    food_model.created_at=food_json['created_at']
    food_model.updated_at=food_json['updated_at']
    

    return food_model

def transform_json_data_into_updatefood_model(
    food_model, food_json):
    #food_model.restaurentId=food_json['restaurentId']
    food_model.name=food_json['name']
    food_model.category=food_json['category']
    food_model.price=food_json['price']
    food_model.description=food_json['description']
    food_model.created_at=food_json['created_at']
    food_model.updated_at=food_json['updated_at']
    

    return food_model

