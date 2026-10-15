"""
apps/products/urls.py: Product Catalog URL Routing
==================================================
Maps catalog-related endpoints to views:
- categories/        -> Category list and creation
- categories/<slug>/ -> Category detail, update, and deletion
- ''                 -> Product listing, filtering, search, and creation
- <slug>/            -> Product detail, update, and deletion
"""

from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView
)

app_name = 'products'

urlpatterns = [
    # Kategoriler
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    # Ürünler
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]
