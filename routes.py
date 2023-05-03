
from api.customers import views as customers_views
from api.customers import service as customers_service
# from api.login import service as login_service1
from api.restaurent import views as restaurent_views
from api.order import views as order_views
from api.payment import views as payment_views
from api.delivery import views as delivery_views
from api.registration_login import views as reg_views


routes_path = [
    customers_views.customers_routes,
    restaurent_views.restaurent_routes, 
    order_views.order_routes, 
    delivery_views.delivery_routes,
    payment_views.payment_routes,
    # login_service1.login_routes,
    reg_views.reg_routes,
    
    
    
    ]