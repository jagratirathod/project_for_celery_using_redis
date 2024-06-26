from __future__  import absolute_import , unicode_literals
import os 
from celery  import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_with_redis.settings')

app = Celery('celery_with_redis')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings , namespace = 'CELERY')


#CELERY BEAT SETTINGS
app.conf.beat_schedule = {
     'send-mail-every-day-at-8' : {
          'task' : 'celery_beat_app.tasks.send_mail_func',
          'schedule': crontab(hour=12, minute=6),  # 15 corresponds to 3 PM      
          # 'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
          # 'args' : (2 ,)    
          }
	}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
     print(f'Request: {self.request}')

