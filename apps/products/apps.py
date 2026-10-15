"""
apps/products/apps.py: Products Application Configuration
=========================================================
Defines the AppConfig specification for the products app.
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'
