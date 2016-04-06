# -*- coding: utf8 -*-
import os

from crawler import image_crawler_settings

BROKER_URL = image_crawler_settings.CRAWLER_BROKER_URL
CELERY_RESULT_BACKEND = image_crawler_settings.CRAWLER_CELERY_RESULT_BACKEND
CELERY_TASK_SERIALIZER='json'
CELERY_TASK_SERIALIZER='pickle'