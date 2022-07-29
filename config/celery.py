from celery import Celery
import os
from celery import shared_task 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app =Celery('my_django_celery_beat')

app.conf.broker_url = 'redis://localhost:6379/0'
app.autodiscover_tasks()

