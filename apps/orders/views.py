"""
apps/orders/views.py: Sipariş API Görünümleri (Views)
====================================================
Sipariş listeleme, yeni sipariş verme ve iptal uç noktalarını yönetir.

Sınıflar:
1. OrderListCreateView (ListCreateAPIView):
   - GET  /api/v1/orders/ -> Giriş yapan kullanıcının sipariş geçmişini getirir (Admin tüm siparişleri görür).
   - POST /api/v1/orders/ -> Sepetteki ürünlerle yeni sipariş oluşturur (Stoktan düşer).
2. OrderDetailView (RetrieveAPIView):
   - GET  /api/v1/orders/<id>/ -> Tek bir siparişin kalemlerini ve kargo detayını döner.
3. OrderCancelView (GenericAPIView):
   - POST /api/v1/orders/<id>/cancel/ -> 'Beklemede' olan siparişi iptal eder ve ürün stoklarını iade eder.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema

from .models import Order, OrderStatus
from .serializers import (
    OrderDetailSerializer,
    OrderCreateSerializer
)


@extend_schema(tags=['Siparişler'], summary="Kullanıcının Siparişlerini Listele veya Yeni Sipariş Ver (Checkout)")
class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET: Giriş yapan kullanıcının kendi sipariş geçmişini listeler.
    POST: Sepetteki ürünlerle sipariş oluşturur (Stoktan düşer).
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().prefetch_related('items__product').select_related('user')
        return Order.objects.filter(user=user).prefetch_related('items__product')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {
                "message": "Siparişiniz başarıyla alındı.",
                "order": OrderDetailSerializer(order).data
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(tags=['Siparişler'], summary="Sipariş Detayı")
class OrderDetailView(generics.RetrieveAPIView):
    """
    Tek bir siparişin kalemlerini ve kargo adresini getirir.
    Kullanıcı sadece kendi siparişini görebilir (Admin tüm siparişleri görebilir).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().prefetch_related('items__product')
        return Order.objects.filter(user=user).prefetch_related('items__product')


@extend_schema(tags=['Siparişler'], summary="Siparişi İptal Et")
class OrderCancelView(generics.GenericAPIView):
    """
    Kullanıcının 'Beklemede' (Pending) olan siparişini iptal etmesini sağlar.
    İptal edilen ürünlerin stokları geri iade edilir.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Sipariş bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        if order.status != OrderStatus.PENDING:
            return Response(
                {"error": f"Sadece 'Beklemede' olan siparişler iptal edilebilir. Mevcut durum: {order.get_status_display()}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Stokları geri iade et
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = OrderStatus.CANCELLED
        order.save()

        return Response({"message": f"#{order.id} numaralı sipariş başarıyla iptal edildi ve stoklar iade edildi."})
