# -*- coding: utf-8 -*-
from .settings_base import *
import platform

if platform.uname()[0] == 'Linux':
    if 'ip-172-31-37-167.us-west-2.compute.internal' in platform.uname()[1]:
        DOMAIN_URL = '52.27.115.131'
        DEBUG = True
        TIME_ZONE = 'UTC'
        HTTPS_SUPPORT = not DEBUG
        SESSION_COOKIE_DOMAIN = '52.27.115.131'
        SESSION_COOKIE_SECURE = not DEBUG

if not DEBUG:
    import mimetypes
    mimetypes.add_type("image/png", ".png", True)
