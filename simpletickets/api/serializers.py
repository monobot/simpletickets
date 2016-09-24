# -*- coding: utf-8 -*-
from rest_framework import serializers

from simpletickets.models import Ticket  # noqa


class UserTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('ticket_type', 'severity', 'description')


class StaffTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('staff', 'ticket_type', 'severity', 'state',
            'resolution_text',
            )
