# -*- coding: utf-8 -*-
import os

from .settings import ST_ATTACHMENTS, ST_ATTACH_URL, MONITOR_FILES_DIR


def monitorfile_url(ticket):
    return ST_ATTACH_URL + '{id}-{user}.mon'.format(
        id=ticket.id, user=ticket.user
        )


def monitorfile(ticket):
    return os.path.join(
        ST_ATTACHMENTS,
        MONITOR_FILES_DIR,
        '{id}-{user}.mon'.format(
            id=ticket.id,
            user=ticket.user,
            )
        )


def monitor(myfilename, msg):
    with open(myfilename, 'a') as monitor:
        monitor.write(msg)
