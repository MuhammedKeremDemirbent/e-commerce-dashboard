"""
apps/orders/urls.py: Sipariş Modülü URL Rotaları
================================================
Sipariş API uç noktalarını tanımlar:
- ''             -> OrderListCreateView (Siparişleri Listele / Sipariş Ver)
- <int:pk>/      -> OrderDetailView (Sipariş Detayı)
- <int:pk>/cancel/ -> OrderCancelView (Siparişi İptal Et ve Stoğu İade Et)
"""

from django.urls import path
from .views import (
    OrderListCreateView,
    OrderDetailView,
    OrderCancelView
)

app_name = 'orders'

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
]
