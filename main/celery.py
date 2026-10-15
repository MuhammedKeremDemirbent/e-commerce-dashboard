"""
main/celery.py: Celery ve Asenkron Görev Konfigürasyonu
======================================================
Bu dosya, projenin asenkron görev kuyruk (task queue) motoru olan Celery'yi yapılandırır.

İçerik ve Görevler:
1. DJANGO_SETTINGS_MODULE değişkenini 'main.settings' olarak tanımlar.
2. Celery uygulamasını 'main' adıyla başlatır.
3. Django ayarlarındaki CELERY_ ön ekiyle başlayan konfigürasyonları okur.
4. apps/ altındaki tüm 'tasks.py' dosyalarındaki görevleri otomatik olarak keşfeder (autodiscover_tasks).
"""

import os
from celery import Celery

# Django settings modülünü Celery'e tanıt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

# settings.py'deki CELERY_ ile başlayan tüm ayarları otomatik yükle
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tüm uygulamalardaki tasks.py dosyalarını otomatik bul
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
