"""
apps/users/views.py: Kullanıcı API Görünümleri (Views)
=====================================================
Kullanıcı kayıt, giriş ve profil isteklerini karşılayan DRF Generic View sınıflarıdır.

Sınıflar ve Endpointler:
1. RegisterView (generics.CreateAPIView):
   - POST /api/v1/auth/register/ -> Yeni hesap oluşturur (Herkese Açık).
2. CustomTokenObtainPairView (TokenObtainPairView):
   - POST /api/v1/auth/login/ -> E-posta ve şifre ile JWT üretir.
3. ProfileView (generics.RetrieveUpdateAPIView):
   - GET /api/v1/auth/profile/   -> Giriş yapmış kullanıcının profilini getirir (IsAuthenticated).
   - PATCH /api/v1/auth/profile/ -> Kullanıcının ad/soyad/telefon bilgilerini günceller.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import User
from .serializers import (
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer
)


@extend_schema(tags=['Kimlik Doğrulama (Auth)'], summary="Yeni Kullanıcı Kaydı")
class RegisterView(generics.CreateAPIView):
    """
    Yeni bir kullanıcı hesabı oluşturur.
    Başarılı kayıtta oluşturulan kullanıcının temel bilgileri döndürülür.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Kullanıcı başarıyla kaydedildi.",
                "user": UserProfileSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(tags=['Kimlik Doğrulama (Auth)'], summary="JWT İle Giriş Yap (Token Al)")
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    E-posta ve şifre ile giriş yaparak 'access' ve 'refresh' token alır.
    """
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    get=extend_schema(tags=['Kullanıcı Profili'], summary="Giriş Yapan Kullanıcının Profilini Getir"),
    put=extend_schema(tags=['Kullanıcı Profili'], summary="Profili Güncelle (Tam Değişiklik)"),
    patch=extend_schema(tags=['Kullanıcı Profili'], summary="Profili Kısmi Güncelle"),
)
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Giriş yapmış olan kullanıcının kendi profil bilgilerini görmesini ve güncellemesini sağlar.
    İstek başlığında 'Authorization: Bearer <access_token>' gönderilmelidir.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
