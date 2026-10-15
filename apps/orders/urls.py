"""
apps/orders/urls.py: Order Module URL Routing
=============================================
Maps order endpoints to views:
- ''             -> OrderListCreateView (List user orders / Create order)
- <int:pk>/      -> OrderDetailView (Retrieve order details)
- <int:pk>/cancel/ -> OrderCancelView (Cancel order and restore inventory)
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
