"""
manage.py: Django Yönetim ve Komut Dosyası
==========================================
Bu dosya, Django projesinin komut satırı aracıdır.
Projeyi ayağa kaldırma, veritabanı tablolarını oluşturma (migration) ve otomatik
testleri çalıştırma gibi tüm yönetimsel işlemler bu dosya üzerinden yürütülür.

Sık Kullanılan Komutlar:
- python manage.py runserver 0.0.0.0:8000 : Geliştirme sunucusunu başlatır.
- python manage.py makemigrations         : Model değişikliklerini tespit edip migration dosyası üretir.
- python manage.py migrate                : Migration'ları veritabanına (PostgreSQL) uygular.
- python manage.py test                   : apps/ altındaki tüm birim ve entegrasyon testlerini koşturur.
- python manage.py createsuperuser        : Sisteme tam yetkili yönetici (admin) hesabı tanımlar.
"""

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
