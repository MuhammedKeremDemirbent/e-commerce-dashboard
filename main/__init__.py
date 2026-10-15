"""
main/__init__.py: Core Package Initializer
=========================================
Ensures the Celery application instance is loaded when Django starts,
allowing the @shared_task decorator to bind automatically.
"""

# Bu dosya Celery'nin Django başlarken otomatik yüklenmesini sağlar
from .celery import app as celery_app

__all__ = ('celery_app',)
