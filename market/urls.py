from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.market_list, name='market_list'),
    
]
