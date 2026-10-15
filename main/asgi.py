"""
main/asgi.py: ASGI Asenkron Web Sunucusu Giriş Noktası
======================================================
Daphne, Uvicorn gibi asenkron (WebSocket, async HTTP) sunucular için giriş noktasıdır.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_asgi_application()
