import os
from celery import Celery

#default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nduggaproject.settings')

app = Celery('nduggaproject')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

