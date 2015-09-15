# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from django.contrib import admin

from views import TicketList, TicketCreate, TicketDelete, TicketUpdate

from simpletickets.settings.ticketSettings import (TICKET_REST_API,
        API_BASE_URL
    )  # noqa

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', TicketList.as_view(), name='ticketList'),
        url(r'^new-ticket/$', TicketCreate.as_view(), name='newTicket'),
        url(r'^edit-ticket-(?P<ticket_id>[\d]*)/$',
                TicketUpdate.as_view(), name='TicketUpdate'
            ),
        url(r'^delete-ticket-(?P<ticket_id>[\d]*)/$',
                TicketDelete.as_view(), name='TicketDelete'
            ),
    )

if TICKET_REST_API:
    urlpatterns += patterns('',
        url(r'^{url}/'.format(url=API_BASE_URL), include('api.urls')),
        )
