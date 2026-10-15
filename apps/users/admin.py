"""
apps/users/admin.py: Kullanıcı Modeli Django Admin Konfigürasyonu
================================================================
Custom User modelinin Django Admin panelinde (/admin/) nasıl listeleneceğini,
arama kriterlerini, filtrelerini ve şifreleme alanlarını yönetir.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Özel Kullanıcı modelimiz için Django Admin panel yapılandırması.
    """
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_verified', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name', 'phone_number', 'address')}),
        ('Yetkiler & İzinler', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Tarih Bilgileri', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name'),
        }),
    )
