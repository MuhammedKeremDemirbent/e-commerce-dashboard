"""
main/wsgi.py: WSGI Web Sunucusu Giriş Noktası
=============================================
Gunicorn, uWSGI veya standart WSGI uyumlu sunucuların projeyi çalıştırması için
kullanılan standart giriş kapısıdır.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_wsgi_application()
