# -*- coding: utf8 -*-
import logging
import sys, os


# 设置 logger
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

try:
    import image_crawler_settings
except:
    sys.path.append(os.path.dirname(os.path.abspath('.')))
    import image_crawler_settings
