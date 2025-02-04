
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
# Include your custom 404 error handler view
from user import views



urlpatterns = [
        
 
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
]

