from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
import os 

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ['DJANGO_CONFIGURATION'] = 'Dev'

__all__ = ("celery_app",)