"""
apps/orders/models.py: Sipariş ve Sipariş Kalemi Veritabanı Modelleri
====================================================================
Bu dosya, sipariş süreçlerinin veritabanı şemasını tanımlar.

Modeller:
1. OrderStatus (TextChoices):
   - PENDING (Beklemede), PROCESSING (Hazırlanıyor), COMPLETED (Tamamlandı), CANCELLED (İptal Edildi).
2. Order:
   - user (ForeignKey -> User): Siparişi veren müşteri.
   - status: Güncel sipariş durumu.
   - total_price: Siparişin toplam fatura tutarı.
   - shipping_address: Teslimat adresi.
3. OrderItem:
   - order (ForeignKey -> Order): Bağlı olduğu sipariş.
   - product (ForeignKey -> Product): Satın alınan ürün.
   - quantity: Sipariş edilen adet.
   - price: Sipariş anındaki birim ürün fiyatı (fiyat değişse bile sipariş tarihi korunur).
"""

from django.conf import settings
from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Beklemede'
    PROCESSING = 'processing', 'Hazırlanıyor'
    SHIPPED = 'shipped', 'Kargoya Verildi'
    DELIVERED = 'delivered', 'Teslim Edildi'
    CANCELLED = 'cancelled', 'İptal Edildi'


class Order(models.Model):
    """
    Sipariş ana tablosu
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name="Kullanıcı"
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Sipariş Durumu"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Toplam Tutar (TL)"
    )
    shipping_address = models.TextField(verbose_name="Teslimat Adresi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sipariş Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        db_table = 'orders'
        verbose_name = 'Sipariş'
        verbose_name_plural = 'Siparişler'
        ordering = ['-created_at']

    def __str__(self):
        return f"Sipariş #{self.id} - {self.user.email} ({self.get_status_display()})"


class OrderItem(models.Model):
    """
    Sipariş içindeki ürün kalemleri.
    Not: 'price' alanı, ürün ileride fiyat değiştirse bile
    satın alındığı andaki fiyatı korumak için saklanır.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name="Sipariş"
    )
    product = models.ForeignKey(
        'products.Product',
        related_name='order_items',
        on_delete=models.PROTECT,
        verbose_name="Ürün"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Birim Fiyat (TL)")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Adet")

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Sipariş Kalemi'
        verbose_name_plural = 'Sipariş Kalemleri'

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Sipariş #{self.order.id})"
