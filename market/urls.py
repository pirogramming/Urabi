from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.market_list, name='market_list'),
    path('create', views.market_create, name='market_create'),
    path('detail/<int:pk>', views.market_detail, name='market_detail'),
    path('update/<int:pk>', views.market_update, name='market_update'),
    path('delete/<int:pk>', views.market_delete, name='market_delete'),
    path("<int:pk>/zzim/", views.market_zzim, name="market_zzim"),

]
