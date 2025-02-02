from django.urls import path
from .views import *

app_name = 'flash'

urlpatterns = [
    path("", flash_list, name="flash_list"),
    path("register/", flash_register, name="flash_register"),
    path('<int:pk>/', flash_detail, name='flash_detail'),
    path("<int:pk>/delete/", flash_delete, name="flash_delete"),
    path("<int:pk>/update/", flash_update, name="flash_update"),
    path("<int:pk>/zzim/", flash_zzim, name="flash_zzim"),
]