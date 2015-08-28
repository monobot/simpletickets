# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.utils.translation import ugettext as _

BASE_TEMPLATE = getattr(settings, 'BASE_TEMPLATE', 'index.html')

TICKET_ATTACHMENTS = getattr(settings, 'TICKET_ATTACHMENTS',
        os.path.join(settings.MEDIA_ROOT, 'tickets'))

TICKET_TYPE = getattr(settings, 'TICKET_TYPE', (
        (1, _(u'Inform about an error')),
        (2, _(u'Problem')),
        (3, _(u'Propose a sugestion')),
        (4, _(u'Others')),
        ))

TICKET_SEVERITY = getattr(settings, 'TICKET_SEVERITY', (
        (1, _(u'Critical')),
        (2, _(u'Very important')),
        (3, _(u'Important')),
        (4, _(u'Normal')),
        ))

TICKET_STATE = getattr(settings, 'TICKET_STATE', (
        (1, _(u'new')),
        (2, _(u'assigned')),
        (3, _(u'solved')),
        (4, _(u'closed')),
        ))
