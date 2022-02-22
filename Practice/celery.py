import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Practice.settings')

app = Celery('Practice',  broker='pyamqp://guest@localhost//')

app.config_from_object('Practice.settings', namespace='CELERY')

app.autodiscover_tasks()


