"""
main/urls.py: Projenin Merkezi Rota Haritası (Root URL Router)
=============================================================
Bu dosya, gelen tüm HTTP isteklerini ilgili uygulamalara veya sayfalara yönlendirir.

Yönlendirmeler:
1. Frontend Arayüz Sayfaları:
   - ''            -> templates/products.html  (Ana Sayfa & Vitrin)
   - 'auth/'       -> templates/auth.html      (Giriş & Kayıt Ekranı)
   - 'orders/'     -> templates/orders.html    (Sipariş Takibi ve İptal)
   - 'profile/'    -> templates/profile.html   (Kullanıcı Bilgileri Düzenleme)
   - 'dashboard/'  -> templates/dashboard.html (Yönetici & Stok Paneli)
2. Yönetim ve Dokümantasyon:
   - 'admin/'      -> Django yerleşik yönetim paneli
   - 'api/docs/'   -> Swagger UI interaktif API test dokümantasyonu
   - 'api/schema/' -> OpenAPI 3.0 YAML/JSON şeması
3. REST API Endpoint Grupları:
   - 'api/v1/auth/'     -> apps.users.urls     (Kayıt, Giriş, Profil, Token Yenileme)
   - 'api/v1/products/' -> apps.products.urls  (Kategoriler, Ürünler, Arama, Stok)
   - 'api/v1/orders/'   -> apps.orders.urls    (Sepet Siparişi Verme, İptal, Geçmiş)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # ─── FRONTEND SAYFALARI (TemplateView) ───────────────────────────
    path('', TemplateView.as_view(template_name='products.html'), name='home'),
    path('auth/', TemplateView.as_view(template_name='auth.html'), name='auth'),
    path('login/', TemplateView.as_view(template_name='auth.html'), name='login'),
    path('orders/', TemplateView.as_view(template_name='orders.html'), name='orders'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),

    # ─── DJANGO ADMIN ────────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ─── SWAGGER / OPENAPI ───────────────────────────────────────────
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # ─── REST API ENDPOINTS ──────────────────────────────────────────
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
