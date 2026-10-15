"""
apps/products/views.py: Product and Category API Views
======================================================
Generic API views handling catalog browsing, filtering, search, and administrative CRUD.

Views:
1. CategoryListCreateView : GET /categories/ (Public), POST /categories/ (Admin only)
2. CategoryDetailView     : GET/PUT/PATCH/DELETE /categories/<slug>/
3. ProductListCreateView  : GET /products/?category=&search=&ordering= (Public), POST /products/ (Admin only)
4. ProductDetailView      : GET/PUT/PATCH/DELETE /products/<slug>/ (Public read, Admin write)
"""

from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer
)


# ─── KATEGORİ VIEW'LERİ ──────────────────────────────────────────

@extend_schema(tags=['Kategoriler'], summary="Kategorileri Listele veya Kategori Ekle (Admin)")
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: Tüm aktif kategorileri listeler (Herkese Açık).
    POST: Yeni kategori ekler (Sadece Admin).
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


@extend_schema(tags=['Kategoriler'], summary="Kategori Detay, Güncelle ve Sil")
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Kategori detayı (Herkese Açık).
    PUT/PATCH/DELETE: Kategori güncelleme veya silme (Sadece Admin).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]


# ─── ÜRÜN VIEW'LERİ ──────────────────────────────────────────────

@extend_schema(tags=['Ürünler'], summary="Ürünleri Listele veya Ürün Ekle (Admin)")
class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET: Ürünleri listeler, filtreler ve arar (Herkese Açık).
    POST: Yeni ürün ekler (Sadece Admin).
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__slug', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


@extend_schema(tags=['Ürünler'], summary="Ürün Detay, Güncelle ve Sil")
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Tek bir ürünün tüm detayları (Herkese Açık).
    PUT/PATCH/DELETE: Ürün bilgilerini güncelle veya sil (Sadece Admin).
    """
    queryset = Product.objects.all().select_related('category')
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
