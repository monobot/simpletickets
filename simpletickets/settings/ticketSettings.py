# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from django.conf import settings
from django.utils.translation import ugettext as _

BASE_TEMPLATE = getattr(settings, 'BASE_TEMPLATE', 'index.html')

TICKET_ATTACHMENTS = getattr(settings, 'TICKET_ATTACHMENTS',
        os.path.join(settings.MEDIA_ROOT, 'tickets'))

DELTA_CLOSE = getattr(settings, 'DELTA_CLOSE', timedelta(minutes=1))
DELTA_CLOSE = getattr(settings, 'DELTA_CLOSE', timedelta(hours=6))

TICKET_TYPE = getattr(settings, 'TICKET_TYPE', (
        (1, _(u'Inform about an error')),
        (2, _(u'Problem')),
        (8, _(u'Propose a sugestion')),
        (9, _(u'Others')),
        ))

TICKET_SEVERITY = getattr(settings, 'TICKET_SEVERITY', (
        (1, _(u'Low')),
        (2, _(u'Normal')),
        (5, _(u'important')),
        (8, _(u'very important')),
        (9, _(u'Critical')),
        ))

TICKET_STATE = getattr(settings, 'TICKET_STATE', (
        (1, _(u'new')),
        (2, _(u'assigned')),
        (5, _(u'in progress')),
        (8, _(u'solved')),
        (9, _(u'closed')),
        ))

TICKET_MNTR_STAFF = getattr(settings, 'TICKET_MNTR_STAFF', True)
TICKET_MNTR_OWNER = getattr(settings, 'TICKET_MNTR_OWNER', False)

STATISTIC_TIMES_STAFF = getattr(settings, 'STATISTIC_TIMES_STAFF', True)
STATISTIC_NUMBERS_STAFF = getattr(settings, 'STATISTIC_NUMBERS_STAFF', True)

STATISTIC_TIMES_OWNER = getattr(settings, 'STATISTIC_TIMES_OWNER', True)
STATISTIC_NUMBERS_OWNER = getattr(settings, 'STATISTIC_NUMBERS_OWNER', True)
