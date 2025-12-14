from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView #Login

# base 
urlpatterns = [
    path('', views.index),
    path('hello', views.hello),
    path('pri_test', views.only_mem),
    path('test', views.test),
    path('login',TokenObtainPairView.as_view() ), # routh login
    path('register', views.register_user),#Register
     
]
