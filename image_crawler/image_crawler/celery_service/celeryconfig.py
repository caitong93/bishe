# -*- coding: utf8 -*-
import os

from celery_service import image_crawler_settings

BROKER_URL = image_crawler_settings.BROKER_URL
CELERY_RESULT_BACKEND = image_crawler_settings.CELERY_RESULT_BACKEND
CELERY_TASK_SERIALIZER='json'