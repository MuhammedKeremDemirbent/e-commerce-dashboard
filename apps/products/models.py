"""
apps/products/models.py: Category and Product Models
====================================================
Defines the relational database models for the product catalog.

Models:
1. Category:
   - name, slug, description, is_active.
   - Automatically generates URL-safe slugs on save.
2. Product:
   - category (ForeignKey -> Category): Associated product category.
   - name, slug, description: Product title, unique slug, and details.
   - price (DecimalField): Decimal precision currency price.
   - stock (PositiveIntegerField): Available inventory count.
   - is_active: Catalog visibility flag.
"""

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Ürün kategorileri (örn: Elektronik, Giyim, Kitap)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        db_table = 'categories'
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    E-ticaret Ürün modeli
    """
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name="Kategori"
    )
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Ürün Açıklaması")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat (TL)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stok Adedi")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Ürün Görseli")
    is_active = models.BooleanField(default=True, verbose_name="Satışta mı?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")

    class Meta:
        db_table = 'products'
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.price} TL)"
