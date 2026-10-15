"""
apps/orders/serializers.py: Order Serializers and Atomic Checkout Logic
=======================================================================
Serializes order data and implements concurrency-safe checkout logic.

Key Classes:
1. OrderItemSerializer: Serializes individual line items within an order.
2. OrderDetailSerializer: Full order representation including status, items, and address.
3. OrderCreateSerializer (Checkout Logic):
   - Wraps checkout in transaction.atomic() with select_for_update() row locking to prevent race conditions.
   - Validates real-time inventory levels against requested quantities.
   - Automatically deducts stock and records order items.
"""

from django.db import transaction
from rest_framework import serializers
from apps.products.models import Product
from .models import Order, OrderItem, OrderStatus


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Sipariş içi ürün kalemi (Görüntüleme için).
    """
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Sipariş Detay ve Listeleme Serializer'ı.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'status', 'status_display',
            'total_price', 'shipping_address', 'items',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')


class OrderItemCreateSerializer(serializers.Serializer):
    """
    Sipariş verirken sepetteki her bir ürün girdisi.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    """
    Sipariş Oluşturma (Checkout) Serializer'ı.
    Stok kontrolü yapar, stok düşer ve siparişi tek bir transaction'da kaydeder.
    """
    shipping_address = serializers.CharField(max_length=500, required=True)
    items = OrderItemCreateSerializer(many=True, required=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Sipariş vermek için en az bir ürün gereklidir.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data['items']
        shipping_address = validated_data['shipping_address']

        product_ids = [item['product_id'] for item in items_data]

        with transaction.atomic():
            # Satır kilitleme (select_for_update) ile stok yarış koşulunu (race condition) önlüyoruz
            products = Product.objects.select_for_update().filter(id__in=product_ids, is_active=True)
            product_map = {p.id: p for p in products}

            # 1. Doğrulama: Tüm ürünler mevcut mu?
            for item in items_data:
                pid = item['product_id']
                if pid not in product_map:
                    raise serializers.ValidationError(f"ID {pid} olan ürün bulunamadı veya satışta değil.")

            # 2. Stok Kontrolü ve Toplam Fiyat Hesabı
            total_price = 0
            for item in items_data:
                product = product_map[item['product_id']]
                qty = item['quantity']
                if product.stock < qty:
                    raise serializers.ValidationError(
                        f"'{product.name}' ürünü için yeterli stok yok! (Kalan stok: {product.stock}, İstenen: {qty})"
                    )
                total_price += product.price * qty

            # 3. Siparişi Oluştur
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                total_price=total_price,
                status=OrderStatus.PENDING
            )

            # 4. Kalemleri Oluştur ve Stokları Düş
            order_items = []
            for item in items_data:
                product = product_map[item['product_id']]
                qty = item['quantity']

                product.stock -= qty
                product.save()

                order_items.append(
                    OrderItem(
                        order=order,
                        product=product,
                        quantity=qty,
                        price=product.price
                    )
                )

            OrderItem.objects.bulk_create(order_items)

        return order
