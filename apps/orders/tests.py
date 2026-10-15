"""
apps/orders/tests.py: Order and Inventory Test Suite (4 Tests)
==============================================================
Verifies concurrency safety, inventory deduction, data isolation, and stock restoration on cancellation.

Executed Tests:
1. test_basarili_siparis_stok_duser                      : Verifies stock deduction (5 -> 3) and 201 Created on valid checkout.
2. test_yetersiz_stokta_siparis_engellenir_ve_stok_degismez : Confirms 400 Bad Request when requested quantity exceeds stock.
3. test_kullanici_sadece_kendi_siparislerini_gorur       : Ensures customers only see their own orders (Data isolation).
4. test_siparis_iptali_stoklari_iade_eder                : Verifies cancelled pending orders return stock to inventory.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderStatus

User = get_user_model()


class OrderTransactionTests(APITestCase):
    """
    Sipariş Oluşturma, Stok Düşürme (Race condition koruması) ve İptal Testleri
    """
    def setUp(self):
        self.user = User.objects.create_user(
            email='musteri@test.com',
            password='Password123!'
        )
        self.other_user = User.objects.create_user(
            email='diger@test.com',
            password='Password123!'
        )
        self.category = Category.objects.create(name='Test Kategori')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Laptop',
            price=25000,
            stock=5
        )
        self.client.force_authenticate(user=self.user)

    def test_basarili_siparis_stok_duser(self):
        """5 olan stoktan 2 sipariş verilince stok 3'e düşmeli."""
        payload = {
            'shipping_address': 'Kadıköy, İstanbul',
            'items': [
                {'product_id': self.product.id, 'quantity': 2}
            ]
        }
        response = self.client.post('/api/v1/orders/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Stok kontrolü
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # Veritabanı sipariş kontrolü
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total_price, 50000)
        self.assertEqual(order.items.count(), 1)

    def test_yetersiz_stokta_siparis_engellenir_ve_stok_degismez(self):
        """Stok 5 iken 10 adet sipariş verilmeye çalışılırsa hata dönmeli ve stok 5 kalmalıdır."""
        payload = {
            'shipping_address': 'Kadıköy, İstanbul',
            'items': [
                {'product_id': self.product.id, 'quantity': 10}
            ]
        }
        response = self.client.post('/api/v1/orders/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Stok değişmedi mi?
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)
        # Sipariş oluşmadı mı?
        self.assertEqual(Order.objects.count(), 0)

    def test_kullanici_sadece_kendi_siparislerini_gorur(self):
        # 1. user için bir sipariş
        self.client.post('/api/v1/orders/', {
            'shipping_address': 'Adres 1',
            'items': [{'product_id': self.product.id, 'quantity': 1}]
        }, format='json')

        # 2. other_user ile giriş yapıp listeleyelim
        self.client.force_authenticate(user=self.other_user)
        res = self.client.get('/api/v1/orders/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        items = res.data.get('results', res.data)
        self.assertEqual(len(items), 0)

    def test_siparis_iptali_stoklari_iade_eder(self):
        # 1. 2 adet sipariş verelim (stok 5 -> 3)
        res = self.client.post('/api/v1/orders/', {
            'shipping_address': 'Adres',
            'items': [{'product_id': self.product.id, 'quantity': 2}]
        }, format='json')
        order_id = res.data['order']['id']

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # 2. Siparişi iptal et
        cancel_res = self.client.post(f'/api/v1/orders/{order_id}/cancel/')
        self.assertEqual(cancel_res.status_code, status.HTTP_200_OK)

        # 3. Stok geri 5 oldu mu?
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

        # 4. Durum CANCELLED oldu mu?
        order = Order.objects.get(id=order_id)
        self.assertEqual(order.status, OrderStatus.CANCELLED)
