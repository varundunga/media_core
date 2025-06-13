import os
import logging

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_core.settings')

logger = logging.getLogger(__name__)
app = Celery('media_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     logger.info(f'Request: {self.request!r}')
#     logger.info('Debug task executed successfully.')
    
# debug_task.delay()