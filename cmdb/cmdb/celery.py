# coding: utf-8
from __future__ import absolute_import, unicode_literals
import os
# from datetime import timedelta
from celery import Celery
# from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb.settings')

app = Celery('cmdb')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sync_machines': {
            'task': 'servers.tasks.sync_machine',
            # 每十分钟执行一次
            # 'schedule': timedelta(minutes=10),
            'schedule': 10.0,
            'args': (),
        },
    }
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
