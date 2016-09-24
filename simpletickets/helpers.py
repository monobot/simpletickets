# -*- coding: utf-8 -*-
import os

from .settings import ST_ATTACHMENTS


def monitorfile(ticket):
    return os.path.join(
        ST_ATTACHMENTS,
        'monitors',
        '{id}-{user}.mon'.format(
            id=ticket.id,
            user=ticket.user,
            )
        )


def monitor(myfilename, msg):
    with open(myfilename, 'a') as monitor:
        monitor.write(msg)
