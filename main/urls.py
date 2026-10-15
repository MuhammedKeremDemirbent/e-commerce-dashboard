"""
main/urls.py: Root URL Routing Configuration
============================================
Routes all incoming HTTP requests to their corresponding views or sub-routers.

Routing Map:
1. Frontend Templates (TemplateView):
   - ''            -> templates/products.html  (Storefront & Product Catalog)
   - 'auth/'       -> templates/auth.html      (Login & Registration)
   - 'orders/'     -> templates/orders.html    (Order Tracking & Cancellation)
   - 'profile/'    -> templates/profile.html   (User Account Profile)
   - 'dashboard/'  -> templates/dashboard.html (Store & Inventory Dashboard)
2. Administrative & Documentation:
   - 'admin/'      -> Django Admin Panel
   - 'api/docs/'   -> Swagger UI interactive API documentation
   - 'api/schema/' -> OpenAPI 3.0 YAML/JSON schema endpoint
3. RESTful API Sub-Routers:
   - 'api/v1/auth/'     -> apps.users.urls     (Auth, JWT Tokens, Profile)
   - 'api/v1/products/' -> apps.products.urls  (Categories, Products, Search)
   - 'api/v1/orders/'   -> apps.orders.urls    (Cart Checkout, Order History)
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
