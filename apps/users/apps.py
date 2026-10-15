"""
apps/users/apps.py: Kullanıcı Uygulaması Yapılandırma Tanımı
============================================================
Django uygulama kaydını (AppConfig) gerçekleştirir.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
