"""
apps/users/urls.py: User Module URL Routing
===========================================
Maps user-related endpoints to views:
- register/      -> RegisterView (User registration)
- login/         -> CustomTokenObtainPairView (JWT authentication)
- token/refresh/ -> TokenRefreshView (Refresh expired access token)
- profile/       -> ProfileView (Retrieve and update profile)
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, ProfileView

app_name = 'users'

urlpatterns = [
    # Kayıt Olma
    path('register/', RegisterView.as_view(), name='register'),
    
    # Giriş Yapma (JWT Access & Refresh Token)
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    
    # Token Yenileme (Refresh Token ile yeni Access Token alma)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Kullanıcı Profili (GET, PUT, PATCH)
    path('profile/', ProfileView.as_view(), name='profile'),
]
