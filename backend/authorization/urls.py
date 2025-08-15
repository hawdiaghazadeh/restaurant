from django.urls import path
from .views import register, change_password , login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('login/', login.as_view() , name='login'),
    path('register/', register.as_view() , name='register'),
    path('change_password/', change_password.as_view() , name='change_password'),
    path('token/refresh/', TokenRefreshView.as_view() , name='token_refresh'),
]