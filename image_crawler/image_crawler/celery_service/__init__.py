# -*- coding: utf8 -*-
import os
import sys

# 存储图片目录
storage = os.path.dirname(os.path.abspath('.')) + '/store'

if not os.path.exists(storage):
    os.mkdir(storage)

try:
    import image_crawler_settings
except:
    sys.path.append(os.path.dirname(os.path.abspath('.')))
    import image_crawler_settings

import scheduler