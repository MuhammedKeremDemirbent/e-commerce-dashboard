"""
apps/products/admin.py: Ürün ve Kategori Django Admin Paneli Tanımları
======================================================================
Kategori ve Ürün modellerinin Django Admin panelinde hiyerarşik listelenmesini,
arama yapılabilmesini, stok miktarının renkli izlenmesini ve slug'ların otomatik dolmasını sağlar.
"""

from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_active')
