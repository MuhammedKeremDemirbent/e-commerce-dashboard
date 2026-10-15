"""
main/__init__.py: Çekirdek Paket Başlatıcı
=========================================
Bu dosya, Django projesi başlatıldığında Celery uygulamasının otomatik olarak
yüklenmesini ve @shared_task dekoratörlerinin bu uygulamayı kullanmasını sağlar.
"""

# Bu dosya Celery'nin Django başlarken otomatik yüklenmesini sağlar
from .celery import app as celery_app

__all__ = ('celery_app',)
