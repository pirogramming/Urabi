from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accompany'

urlpatterns = [
    path('', views.accompany_list, name='accompany_list'),
    path('detail', views.accompany_detail, name='accompany_detail'),
]
