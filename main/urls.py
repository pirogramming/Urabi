from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.shortcuts import render
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.main_view, name='home'),
]

