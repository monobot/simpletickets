# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from django.conf import settings
from django.utils.translation import ugettext as _

BASE_TEMPLATE = getattr(settings, 'BASE_TEMPLATE', 'index.html')

ST_REST_API = getattr(settings, 'ST_REST_API', True)

API_BASE_URL = getattr(settings, 'API_BASE_URL', 'api')

ST_STAFF_GNAME = getattr(settings, 'ST_STAFF_GNAME', 'simpleticket_staff')
ST_ADMIN_GNAME = getattr(settings, 'ST_ADMIN_GNAME', 'simpleticket_admin')

MONITOR_FILES_DIR = 'monitors'
ATTACHMENTS_DIR = 'tickets'

ST_ATTACHMENTS = os.path.join(settings.MEDIA_ROOT, ATTACHMENTS_DIR)

ST_ATTACH_URL = '{media_url}/{attachments_dir}/{monitor_files_dir}/'.format(
    media_url=settings.MEDIA_URL,
    attachments_dir=ATTACHMENTS_DIR,
    monitor_files_dir=MONITOR_FILES_DIR,
    )

ST_DELTA_CLOSE = getattr(settings, 'ST_DELTA_CLOSE', timedelta(hours=6))

ST_TCKT_TYPE = getattr(
    settings,
    'ST_TCKT_TYPE',
    (
        (1, _(u'Inform about an error')),
        (2, _(u'Problem')),
        (8, _(u'Propose a sugestion')),
        (9, _(u'Others')),
        )
    )

ST_TCKT_SEVERITY = getattr(
    settings,
    'ST_TCKT_SEVERITY',
    (
        (1, _(u'Low')),
        (2, _(u'Normal')),
        (5, _(u'important')),
        (8, _(u'very important')),
        (9, _(u'Critical')),
        )
    )

ST_TCKT_STATE = getattr(
    settings,
    'ST_TCKT_STATE',
    (
        (1, _(u'new')),
        (2, _(u'assigned')),
        (5, _(u'in progress')),
        (8, _(u'solved')),
        (9, _(u'closed')),
        )
    )

ST_FL_MNTR_STAFF = getattr(settings, 'ST_FL_MNTR_STAFF', True)
ST_FL_MNTR_OWNER = getattr(settings, 'ST_FL_MNTR_OWNER', False)

ST_SETT_MAIN_TASKBAR = getattr(
    settings, 'ST_SETT_MAIN_TASKBAR', True
    )

ST_SETT_TIMES_STAFF = getattr(
    settings, 'ST_SETT_TIMES_STAFF', True
    )
ST_SETT_NUMBERS_STAFF = getattr(
    settings, 'ST_SETT_NUMBERS_STAFF', True
    )

ST_SETT_TIMES_OWNER = getattr(
    settings, 'ST_SETT_TIMES_OWNER', True
    )
ST_SETT_NUMBERS_OWNER = getattr(
    settings, 'ST_SETT_NUMBERS_OWNER', True
    )
