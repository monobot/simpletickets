# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Ticket, ResponseTicket  # noqa


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
            'ticket_number',
            'user',
            'state',
            'severity',
            'ticket_type',
            'creation_date'
            )
    list_filter = (
            'severity',
            'creation_date',
            'ticket_type',
            )


@admin.register(ResponseTicket)
class ResponseTicketAdmin(admin.ModelAdmin):
    list_display = (
            'staff',
            'state',
            'severity',
            'ticket_type',
            'creation_date'
            )
    list_filter = (
            'staff',
            'asigned_to',
            'severity',
            'creation_date',
            'ticket_type',
            )
