"""
apps/products/urls.py: Ürün ve Kategori URL Rotaları
====================================================
Katalog API uç noktalarını tanımlar:
- categories/        -> Kategori Listeleme & Ekleme
- categories/<slug>/ -> Kategori Detay, Güncelleme & Silme
- ''                 -> Ürün Listeleme, Filtreleme & Ekleme
- <slug>/            -> Ürün Detay, Güncelleme & Silme
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
