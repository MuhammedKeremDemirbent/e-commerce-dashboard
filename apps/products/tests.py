"""
apps/products/tests.py: Product Catalog Test Suite (4 Tests)
============================================================
Verifies catalog accessibility, administrative write protection, and search functionality.

Executed Tests:
1. test_herkes_kategorileri_ve_urunleri_listeleyebilir : Confirms public access to products and categories.
2. test_standart_kullanici_urun_ekleyemez              : Ensures non-staff customers receive 403 Forbidden on product creation.
3. test_admin_yeni_urun_ekleyebilir                    : Verifies administrative users can successfully create products (201).
4. test_arama_filtresi_calisir                         : Tests that ?search= query parameter correctly filters products.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from apps.products.models import Category, Product

User = get_user_model()


class ProductCatalogTests(APITestCase):
    """
    Kategori ve Ürün Listeleme, Yetkilendirme ve Arama Testleri
    """
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email='admin@test.com',
            password='AdminPassword123!'
        )
        self.normal_user = User.objects.create_user(
            email='musteri@test.com',
            password='UserPassword123!'
        )
        self.category = Category.objects.create(
            name='Akıllı Telefonlar',
            description='Telefon kategorisi'
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name='Samsung Galaxy A32',
            price=12000,
            stock=15,
            description='Samsung telefon'
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='iPhone 15 Pro',
            price=65000,
            stock=5,
            description='Apple telefon'
        )

    def test_herkes_kategorileri_ve_urunleri_listeleyebilir(self):
        # 1. Kategoriler (Girişsiz)
        cat_res = self.client.get('/api/v1/products/categories/')
        self.assertEqual(cat_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(cat_res.data.get('results', cat_res.data)) >= 1)

        # 2. Ürünler (Girişsiz)
        prod_res = self.client.get('/api/v1/products/')
        self.assertEqual(prod_res.status_code, status.HTTP_200_OK)
        items = prod_res.data.get('results', prod_res.data)
        self.assertEqual(len(items), 2)

    def test_standart_kullanici_urun_ekleyemez(self):
        """Ürün ekleme sadece Admin yetkisindedir."""
        self.client.force_authenticate(user=self.normal_user)
        payload = {
            'category': self.category.id,
            'name': 'Yetkisiz Ürün',
            'price': 1000,
            'stock': 10
        }
        response = self.client.post('/api/v1/products/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_yeni_urun_ekleyebilir(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            'category': self.category.id,
            'name': 'Xiaomi 14 Ultra',
            'price': 45000,
            'stock': 8,
            'description': 'Xiaomi amiral gemisi'
        }
        response = self.client.post('/api/v1/products/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Xiaomi 14 Ultra').exists())

    def test_arama_filtresi_calisir(self):
        response = self.client.get('/api/v1/products/?search=Galaxy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get('results', response.data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'Samsung Galaxy A32')
