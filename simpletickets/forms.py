# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from .models import Ticket
from .settings import ST_TCKT_STATE


class TicketFormUser(forms.ModelForm):
    class Meta(object):
        model = Ticket
        fields = ('ticket_type', 'severity', 'description')

    def clean_description(self):
        text = self.cleaned_data['description']

        if text == '...':
            raise forms.ValidationError(
                    _(u'Please explain the problem'))
        if len(text.split(' ')) < 5:
            raise forms.ValidationError(
                    _(u'Please expose your problem rigorously'))
        return text


class TicketFormStaff(forms.ModelForm):
    class Meta(object):
        model = Ticket
        fields = ('staff', 'ticket_type', 'severity', 'state',
            'resolution_text',
            )

    def clean_resolution_text(self):
        text = self.cleaned_data['resolution_text']

        if len(text.split(' ')) < 5:
            raise forms.ValidationError(
                    _(u'Please be extensive on the explanation'))
        return text

    def __init__(self, *args, **kwargs):
        super(TicketFormStaff, self).__init__(*args, **kwargs)
        CHOICES = list(ST_TCKT_STATE)[1:-1]
        self.fields['state'].choices = CHOICES
