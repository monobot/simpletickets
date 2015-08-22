# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from views import (TicketList, TicketCreate, TicketDetails, TicketDelete,
        TicketEdit)

admin.autodiscover()

urlpatterns = patterns(
    url(r'^ticket-List/$', TicketList.as_view(), name='ticketList'),
    url(r'^ticket-detail-(?P<ticket_id>[\d]*)/$',
            TicketDetails.as_view(), name='ticketDetails'),
    url(r'^new-ticket/$', TicketCreate, name='newTicket'),
    url(r'^edit-ticket-(?P<ticket_id>[\d]*)/$',
            TicketEdit.AS_view(), name='ticketEdit'),
    url(r'^edit-ticket-(?P<ticket_id>[\d]*)/$',
            TicketDelete.AS_view(), name='ticketEdit'),

    )
