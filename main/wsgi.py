"""
main/wsgi.py: WSGI Server Entrypoint
====================================
Exposes the WSGI callable as a module-level variable named 'application'.
Used by production WSGI web servers (Gunicorn, uWSGI) to serve the project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_wsgi_application()
