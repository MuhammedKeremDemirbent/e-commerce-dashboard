"""
main/asgi.py: ASGI Server Entrypoint
====================================
Exposes the ASGI callable as a module-level variable named 'application'.
Used for handling asynchronous protocols, WebSockets, and async HTTP servers.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_asgi_application()
