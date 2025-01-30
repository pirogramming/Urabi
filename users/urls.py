from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/form/', signup_page, name='signup_form'),
    path('login/form/', login_page, name='login_form'),
]