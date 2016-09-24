# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Ticket  # noqa


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_number',
        'user',
        'staff',
        'state',
        'severity',
        'ticket_type',
        'creation_date',
        )
    list_filter = (
        'user',
        'staff',
        'severity',
        'creation_date',
        'ticket_type',
        'creation_date',
        )
