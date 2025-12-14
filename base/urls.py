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
    path('buy', views.buy),
    path('my_orders', views.my_orders),
    # path('login',TokenObtainPairView.as_view() ), # routh login
    path('login',views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register', views.register_user),#Register
     
]
