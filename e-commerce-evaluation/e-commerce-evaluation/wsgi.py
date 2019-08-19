"""
WSGI config for e-commerce-evaluation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from os.path import join, dirname, abspath

PROJECT_DIR = dirname(dirname(abspath(__file__)))
import sys
sys.path.insert(0,PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e-commerce-evaluation.settings')

application = get_wsgi_application()




