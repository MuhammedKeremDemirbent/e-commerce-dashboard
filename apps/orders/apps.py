"""
apps/orders/apps.py: Sipariş Uygulaması Yapılandırma Tanımı
===========================================================
Django uygulama kaydını (AppConfig) gerçekleştirir.
"""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'
