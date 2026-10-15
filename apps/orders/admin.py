"""
apps/orders/admin.py: Sipariş Django Admin Paneli Tanımları
===========================================================
Siparişlerin (Order) ve sipariş kalemlerinin (OrderItem - TabularInline)
Django Admin panelinde incelenmesini, durum güncellemesini ve filtrelerini yönetir.
"""

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__email', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
