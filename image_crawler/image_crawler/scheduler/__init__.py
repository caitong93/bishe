# -*- coding: utf8 -*-
import os
import sys

try:
    import image_crawler_settings
except:
    sys.path.append(os.path.dirname(os.path.abspath('.')))
    import image_crawler_settings
