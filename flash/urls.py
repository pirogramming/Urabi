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
    path('add_participant/', add_flash_participant, name="add_flash_participant"),
    path('remove_participant/', remove_flash_participant, name="remove_flash_participant"),
    path('apply_participant/', apply_flash_participant, name="apply_flash_participant"),
    path('cancel_participant/', cancel_flash_participant, name="cancel_flash_participant"),
    path('<int:flash_id>/requests/', get_flash_requests, name="get_flash_requests"),
]