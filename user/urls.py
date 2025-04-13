
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from user.views import user_home,products,about_company,terms_condition,contact_us,checkout,order_request,confirmation

urlpatterns = [
        
 
    path('',user_home,name="user_home"),
    path('products/',products,name="products"),
    path('about-company/',about_company,name='about_company'),
    path('terms-and-condition/',terms_condition,name="terms_condition"),
    path('contact-us/',contact_us,name='contact_us'),
    path('checkout/',checkout,name="checkout"),
    path('order-request/',order_request,name="order_request"),
    path('thank-you/order-recieved=<str:oid>/',confirmation,name='confirmation')
       
]

