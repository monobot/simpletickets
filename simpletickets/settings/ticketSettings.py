# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from django.conf import settings
from django.utils.translation import ugettext as _

BASE_TEMPLATE = getattr(settings, 'BASE_TEMPLATE', 'index.html')

TICKET_ATTACHMENTS = getattr(settings, 'TICKET_ATTACHMENTS',
        os.path.join(settings.MEDIA_ROOT, 'tickets'))

DELTA_CLOSE = getattr(settings, 'DELTA_CLOSE', timedelta(hours=12))
DELTA_CLOSE = getattr(settings, 'DELTA_CLOSE', timedelta(minutes=1))

TICKET_TYPE = getattr(settings, 'TICKET_TYPE', (
        (1, _(u'Inform about an error')),
        (2, _(u'Problem')),
        (3, _(u'Propose a sugestion')),
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
        (5, _(u'delayed')),
        (8, _(u'solved')),
        (9, _(u'closed')),
        ))


def monitorfile(ticket):
    return os.path.join(settings.MEDIA_ROOT, 'simpletickets',
            '{id}-{user}-{date}.mon'.format(
                id=ticket.id,
                user=ticket.user,
                date=ticket.creation_date.strftime('%y%m%d'),
            ))


def monitor(myfilename, msg):
    with open(myfilename, 'a') as monitor:
        monitor.write(msg)
