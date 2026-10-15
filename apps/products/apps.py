"""
apps/products/apps.py: Ürün Uygulaması Yapılandırma Tanımı
==========================================================
Django uygulama kaydını (AppConfig) gerçekleştirir.
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'
