# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Ticket, Comunicacion


class TicketAdmin(admin.ModelAdmin):
    list_display = ('usuario_asoc',
                    'tipo',
                    'fecha_creacion'
                    )
    list_filter = (
                'tipo',
                'fecha_creacion')


class ComunicacionAdmin(admin.ModelAdmin):
    list_display = ('usuario_asoc',
                    'comunidad_asoc',
                    'propietario_asoc',
                    'estado',
                    'tipo',
                    'fecha_creacion'
                    )
    list_filter = (
                'estado',
                'tipo',
                'comunidad_asoc',
                'fecha_creacion')


l_admin = [
            (Ticket, TicketAdmin),
            (Comunicacion, ComunicacionAdmin)
            ]
for clase, claseadmin in l_admin:
    admin.site.register(clase, claseadmin)
