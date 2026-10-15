"""
apps/users/serializers.py: Kullanıcı Serileştiricileri (Serializers)
===================================================================
JSON verilerini Python nesnelerine, veritabanı kayıtlarını da JSON formatına dönüştürür.

İçerik:
1. UserRegisterSerializer: Yeni kullanıcı kaydı; şifre onay kontrolü ve parola şifreleme (make_password).
2. CustomTokenObtainPairSerializer: JWT login işlemi; access & refresh token yanında kullanıcı bilgilerini döner.
3. UserProfileSerializer: Kullanıcının profil bilgilerini (ad, soyad, telefon) görüntüleme ve güncelleme (PATCH).
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Kullanıcı Kayıt Serializer'ı.
    Şifre eşleşmesini doğrular ve kullanıcıyı güvenli şekilde oluşturur.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        label="Şifre"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Şifre Tekrar"
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'password_confirm')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Şifreler birbiriyle eşleşmiyor."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        # User manager'daki create_user metodunu kullanarak şifreyi güvenle hash'liyoruz
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT Giriş Serializer'ı.
    Token'ların yanına kullanıcı detaylarını da yanıt olarak ekler.
    """
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)

        # Yanıta kullanıcı bilgilerini ekle
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_staff': self.user.is_staff,
        }
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Giriş yapmış kullanıcının profilini görüntüleme ve güncelleme Serializer'ı.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'is_verified', 'created_at')
        read_only_fields = ('id', 'email', 'is_verified', 'created_at')
