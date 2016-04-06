# -*- coding: utf8 -*-

# scheduler 配置
redis_host = '127.0.0.1'    # 替换为 scheduler 的内网ip
redis_port = '6379'

# SCHEDULER_BROKER_URL = 'redis://localhost:6379/0'
SCHEDULER_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
SCHEDULER_CELERY_RESULT_BACKEND = 'redis://localhost'

# crawler 配置
CRAWLER_BROKER_URL = 'redis://localhost:6379/0'
CRAWLER_CELERY_RESULT_BACKEND = 'redis://localhost'
