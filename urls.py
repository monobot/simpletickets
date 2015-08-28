# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from views import (TicketList, TicketCreate, TicketDelete,
        ResponseTicketCreate, )

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^ticket-list/$', TicketList.as_view(), name='ticketList'),
    url(r'^new-ticket/$', TicketCreate.as_view(), name='newTicket'),
    url(r'^response-ticket-(?P<ticket_id>[\d]*)/$',
            ResponseTicketCreate.as_view(), name='TicketResponse'),
    # url(r'^edit-ticket-(?P<ticket_id>[\d]*)/$',
    #         TicketUpdate.as_view(), name='TicketUpdate'),
    url(r'^delete-ticket-(?P<ticket_id>[\d]*)/$',
            TicketDelete.as_view(), name='TicketDelete'),
    )
