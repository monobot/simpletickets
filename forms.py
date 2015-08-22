# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms
from django.utils.translation import ugettext as _

from models import Ticket, Comunicacion
from ..comunidad.ayudas import decorate_bound_field
decorate_bound_field()


def numret(num):
    return (('0' * 10) + str(num))[-6:]


class TicketForm(forms.ModelForm):
    class Meta(object):
        model = Ticket
        fields = ('tipo', 'texto_creacion',)
        widgets = {'fecha_creacion': forms.DateInput(format='%d/%m/%Y',
                    attrs={'class': 'datePicker', 'readonly': 'true'}), }

    def __init__(self, usuario, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.usuario = usuario

    def clean_texto_creacion(self):
        texto = self.cleaned_data['texto_creacion']

        if texto == '...':
            raise forms.ValidationError(_(u'Explique su problema'))
        if len(texto.split(' ')) < 5:
            raise forms.ValidationError(_(u'Por favor, extiéndase en su ' +
                        u'explicación'))
        return texto

    def save(self, commit=True):
        ahora = datetime.now()
        ticket = super(TicketForm, self).save(commit=False)
        ticket.usuario_asoc = self.usuario
        ticket.fecha_creacion = ahora
        ticket.estado = '1'

        if commit:
            ticket.save()
        ticket.numero_ticket = '%s%s' % (str(ahora.year)[2:],
                    numret(ticket.id))
        ticket.save()
        return ticket


class TicketAdmin(forms.ModelForm):
    class Meta(object):
        model = Ticket
        fields = ('texto_resolucion', 'estado')
        widgets = {'fecha_creacion': forms.DateInput(format='%d/%m/%Y',
                    attrs={'class': 'datePicker', 'readonly': 'true'}), }

    def __init__(self, usuario, *args, **kwargs):
        super(TicketAdmin, self).__init__(*args, **kwargs)
        self.usuario = usuario

    def clean_texto_resolucion(self):
        texto = self.cleaned_data['texto_resolucion']

        if len(texto.split(' ')) < 5:
            raise forms.ValidationError(_(u'Se riguroso en la explicación'))
        return texto

    def save(self, commit=True):
        ticket = super(TicketAdmin, self).save(commit=False)
        ticket.admin_resolucion = self.usuario
        ticket.fecha_resolucion = datetime.now()

        if commit:
            ticket.save()
        return ticket


class ComunicacionForm(forms.ModelForm):
    class Meta(object):
        model = Comunicacion
        fields = ('tipo', 'texto_creacion',)
        widgets = {'fecha_creacion': forms.DateInput(format='%d/%m/%Y',
                    attrs={'class': 'datePicker', 'readonly': 'true'}), }

    def __init__(self, usuario, comunidad, *args, **kwargs):
        super(ComunicacionForm, self).__init__(*args, **kwargs)
        self.usuario = usuario
        self.comunidad = comunidad

    def save(self, commit=True):
        comunicacion = super(ComunicacionForm, self).save(commit=False)
        comunicacion.propietario_asoc = self.usuario
        comunicacion.comunidad_asoc = self.comunidad
        comunicacion.fecha_creacion = datetime.now()
        comunicacion.estado = '1'

        if commit:
            comunicacion.save()
        return comunicacion


class ComunicacionEdita(forms.ModelForm):
    class Meta(object):
        model = Comunicacion
        fields = ('texto_resolucion', 'estado')
        widgets = {'fecha_creacion': forms.DateInput(format='%d/%m/%Y',
                    attrs={'class': 'datePicker', 'readonly': 'true'}), }

    def __init__(self, usuario, *args, **kwargs):
        super(ComunicacionEdita, self).__init__(*args, **kwargs)
        self.usuario = usuario

    def save(self, commit=True):
        comunicacion = super(ComunicacionEdita, self).save(commit=False)
        comunicacion.usuario_asoc = self.usuario
        comunicacion.fecha_resolucion = datetime.now()

        if commit:
            comunicacion.save()
        return comunicacion
