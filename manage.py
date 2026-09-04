#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventbuzz.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Be sure you're in a virtual environment "
            "and have Django installed (pip install django)."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
