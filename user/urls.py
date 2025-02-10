
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from user.views import user_home,checkout,order_request

urlpatterns = [
        
    path('',user_home,name="user_home"),
    path('checkout/',checkout,name="checkout"),
    path('order-request/',order_request,name="order_request"),
]

