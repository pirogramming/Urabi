from django.urls import path
from .views import *

urlpatterns = [
    path('list/', flash_list, name='flash_list'),
    path("register/", flash_register, name="flash_register"),
    path('<int:pk>/', flash_detail, name='flash_detail'),
]