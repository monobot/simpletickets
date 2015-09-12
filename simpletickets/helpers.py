# -*- coding: utf-8 -*-
import os

from django.conf import settings


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
