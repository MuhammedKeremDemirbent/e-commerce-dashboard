"""
apps/users/urls.py: Kullanıcı Modülü URL Rotaları
=================================================
Kullanıcı işlemleriyle ilgili API uç noktalarını tanımlar:
- register/      -> RegisterView (Kayıt)
- login/         -> CustomTokenObtainPairView (JWT Giriş)
- token/refresh/ -> TokenRefreshView (Token Yenileme)
- profile/       -> ProfileView (Profil Bilgileri)
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
