# -*- coding: utf8 -*-
from __future__ import absolute_import

from celery import Celery, platforms

app = Celery('scheduler',
             include=['scheduler.tasks'])
app.config_from_object('scheduler.celeryconfig')

# todo: 采用更好的解决方式
platforms.C_FORCE_ROOT = True

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()