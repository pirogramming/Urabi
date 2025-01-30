from django.urls import path
from .views import flash_list

urlpatterns = [
    path('list/', flash_list, name='flash_list'),
]