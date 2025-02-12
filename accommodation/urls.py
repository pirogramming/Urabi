from django.urls import path
from . import views

app_name = "accommodation"

urlpatterns = [
    path("", views.accommodation_filter, name="filter"), 
    path("create/", views.accommodation_create, name="accommodation_create"), 
    path("<int:pk>/", views.accommodation_review_detail, name="accommodation_review_detail"),  
    #path("location/", views.accommodation_location, name="accommodation_location"),  
    path("<int:pk>/review/create/", views.accommodation_review_create, name="accommodation_review_create"),
    path('review/<int:pk>/update/', views.accommodation_review_update, name='accommodation_review_update'),
    path('review/<int:pk>/delete/', views.accommodation_review_delete, name='accommodation_review_delete'),
    path('review/<int:pk>/toggle_favorite/', views.accommodation_toggle_favorite, name='toggle_favorite'),
    path('review/<int:pk>/toggle_like/', views.accommodation_toggle_like, name='toggle_like'),
]