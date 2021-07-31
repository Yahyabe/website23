from django.urls import path
from Orderapp.views import Add_to_Shoping_cart, cart_detials, cart_delete, OrderCart, Order_showing, Order_Product_showing, user_order_details, userorderproduct_details



urlpatterns = [
    path('addingcart/<int:id>/', Add_to_Shoping_cart, name='Add_to_Shoping_cart'),
    path('cart_detials/', cart_detials, name='cart_detials'),
    path('cart_delete/<int:id>/', cart_delete, name='cart_delete'),
    path('order_cart/', OrderCart, name="OrderCart"),
    path('orderlist/', Order_showing, name="orderlist"),
    path('OrderProduct/', Order_Product_showing, name="orderproduct"),
    path('OrderDetails/<int:id>/', user_order_details, name="user_order_details"),
    path('OrderProductDetails/<int:id>/<int:oid>/', userorderproduct_details, name="userorderproduct_details"),


]         