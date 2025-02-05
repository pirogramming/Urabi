from django.urls import path
from . import views

app_name = "accommodation"

urlpatterns = [
    path("", views.accommodation_filter, name="filter"), 
    path("create/", views.accommodation_create, name="accommodation_create"), 
    path("<int:pk>/", views.accommodation_review_detail, name="accommodation_review_detail"),  
    path("location/", views.accommodation_location, name="accommodation_location"),  
]