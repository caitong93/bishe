# -*- coding: utf8 -*-
import os

from scheduler import image_crawler_settings

BROKER_URL = image_crawler_settings.SCHEDULER_BROKER_URL
# CELERY_RESULT_BACKEND = image_crawler_settings.SCHEDULER_CELERY_RESULT_BACKEND
# CELERY_TASK_SERIALIZER='json'
CELERY_TASK_SERIALIZER='pickle'