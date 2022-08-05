from celery import Celery
import os
from celery import shared_task 
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app =Celery('my_django_celery_beat')
temp_db_redis = config('redisHost')
app.conf.broker_url = f'redis://{temp_db_redis}:6379/0'
app.autodiscover_tasks()

