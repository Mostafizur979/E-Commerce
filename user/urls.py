
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from user.views import user_home

urlpatterns = [
        
    path('',user_home,name="user_home"),
    
]

