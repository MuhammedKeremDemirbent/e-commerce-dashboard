"""
apps/products/serializers.py: Kategori ve Ürün Serileştiricileri
================================================================
Katalog verilerinin JSON dönüşümlerini ve giriş doğrulamasını yapar.

İçerik:
1. CategorySerializer: Kategori adı, slug, açıklama ve ürün sayısı.
2. ProductListSerializer: Vitrin için sadeleştirilmiş ürün kartı verisi.
3. ProductDetailSerializer: Kategori detaylarıyla birlikte tam ürün bilgisi.
4. ProductCreateUpdateSerializer: Ürün ekleme ve düzenleme doğrulayıcısı (fiyat ve stok kontrolü).
"""

from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Kategori Listeleme ve Oluşturma Serializer'ı.
    """
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'products_count', 'is_active', 'created_at')
        read_only_fields = ('id', 'slug', 'created_at')


class ProductListSerializer(serializers.ModelSerializer):
    """
    Ürün Listeleme (Vitrin) Serializer'ı.
    Performans için hafif tutulmuştur.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'category_name', 'price', 'stock', 'image', 'is_active')


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Ürün Detay Sayfası Serializer'ı.
    Kategori detaylarını ve ürün açıklamasını içerir.
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'category', 'description',
            'price', 'stock', 'image', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Ürün Ekleme ve Güncelleme Serializer'ı (Sadece Admin).
    """
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'stock', 'image', 'is_active')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ürün fiyatı 0 TL veya daha az olamaz.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stok adedi negatif olamaz.")
        return value
