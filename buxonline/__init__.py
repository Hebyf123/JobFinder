from __future__ import absolute_import, unicode_literals

# Убедитесь, что задачи Celery загружаются
from .celery import app as celery_app

__all__ = ('celery_app',)
