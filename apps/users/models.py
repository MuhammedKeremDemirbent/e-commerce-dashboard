"""
apps/users/models.py: Custom User Model and Manager
===================================================
Defines the user identity model for the e-commerce system.

Classes:
1. UserManager (BaseUserManager):
   - Uses email as the unique primary identifier instead of standard username.
   - Provides helper methods for create_user() and create_superuser().
2. User (AbstractUser):
   - email         : Unique email address used for authentication (USERNAME_FIELD).
   - phone_number  : Optional customer contact phone number.
   - address       : Default shipping and billing address.
   - is_verified   : Email confirmation verification flag.
   - created_at    : Account creation timestamp.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    E-posta adresini birincil kimlik doğrulama alanı olarak
    kullanan özel kullanıcı yöneticisi.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Kullanıcı oluşturmak için e-posta adresi zorunludur.")
        email = self.normalize_email(email)
        
        # Eğer username verilmediyse e-postanın ön ekini ata
        username = extra_fields.pop('username', None)
        if not username:
            username = email.split('@')[0]
        
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Süper kullanıcı için is_staff=True olmalıdır.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Süper kullanıcı için is_superuser=True olmalıdır.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    E-ticaret projesi için genişletilmiş özel Kullanıcı modeli.
    """
    # Username alanını opsiyonel yapıp email'i temel yapıyoruz
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Kullanıcı Adı")
    email = models.EmailField(unique=True, verbose_name="E-posta Adresi")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon Numarası")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    is_verified = models.BooleanField(default=False, verbose_name="E-posta Doğrulandı mı?")
    
    # Audit log / Zaman damgaları
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # createsuperuser sırasında email ve parola sorulması yeterli

    class Meta:
        db_table = 'users'
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
