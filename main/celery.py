"""
main/celery.py: Celery Configuration and Task Discovery
======================================================
Configures the Celery distributed task queue application.

Responsibilities:
1. Sets default DJANGO_SETTINGS_MODULE to 'main.settings'.
2. Instantiates Celery application as 'main'.
3. Reads configuration from Django settings with 'CELERY_' prefix.
4. Automatically discovers tasks from all installed apps (autodiscover_tasks).
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
