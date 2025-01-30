from django.urls import path
from . import views

app_name = 'accommodation'

urlpatterns = [
    path('', views.accommodation_filter, name='filter'),
]