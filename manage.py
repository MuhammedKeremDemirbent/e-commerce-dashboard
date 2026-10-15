"""
manage.py: Django Command-Line Management Utility
=================================================
This file serves as the administrative entry point for executing Django tasks.

Common Commands:
- python manage.py runserver 0.0.0.0:8000 : Starts the local development server.
- python manage.py makemigrations         : Inspects model changes and generates migration files.
- python manage.py migrate                : Applies database migrations to PostgreSQL.
- python manage.py test                   : Executes automated unit and integration tests.
- python manage.py createsuperuser        : Provisions a new administrative user.
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
