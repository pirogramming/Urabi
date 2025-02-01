from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.market_list, name='market_list'),
    path('create', views.market_create, name='market_create'),
    path('detail_guest', views.market_detail_guest, name='market_detail_guest'),
    path('detail_self', views.market_detail_self, name='market_detail_self'),
]
