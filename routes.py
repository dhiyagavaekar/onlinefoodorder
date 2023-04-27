
from api.customers import views as customers_views
# from api.login import service as login_service
from api.restaurent import views as restaurent_views
from api.order import views as order_views
from api.payment import views as payment_views
from api.delivery import views as delivery_views
from api.login1 import service as login_service


routes_path = [
    customers_views.customers_routes,
    restaurent_views.restaurent_routes, 
    order_views.order_routes, 
    delivery_views.delivery_routes,
    payment_views.payment_routes,
    # login_service.login_routes,
    login_service.login_routes1,
    
    
    
    ]