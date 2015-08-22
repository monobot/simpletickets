# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as ugl

from ..usuario.models import Usuario
from ..comunidad.models import Comunidad
from django.utils.safestring import mark_safe


tipo_ticket = (('1', _(u'nueva')),
            ('2', _(u'resolviendo')),
            ('3', _(u'resuelta')),
            ('4', _(u'cerrada')))

tipo_comunicacion = (('1', _(u'comunicación de avería')),
            ('2', _(u'comunicación de incidencia')),
            ('3', _(u'queja')),
            ('4', _(u'propuesta')),
            ('5', _(u'a debatir')))

tipo_incidencia = (('1', _(u'Informar de un error')),
            ('2', _(u'Problema')),
            ('3', _(u'Proponer una sugerencia')),
            ('4', _(u'Otros motivos')))


class Ticket(models.Model):
    '''Es la clase de las incidencias generales'''
    usuario_asoc = models.ForeignKey(Usuario,
                related_name='usr')

    numero_ticket = models.CharField(max_length=8,
                blank=True,
                null=True)

    tipo = models.CharField(max_length=1,
                choices=tipo_incidencia)
    estado = models.CharField(max_length=1,
                choices=tipo_ticket)

    fecha_creacion = models.DateTimeField(ugl(u'Fecha'))
    texto_creacion = models.TextField(ugl(u'Explicación'),
                default='...')

    fecha_resolucion = models.DateTimeField(ugl(u'Fecha'),
                blank=True,
                null=True)
    texto_resolucion = models.TextField(ugl(u'Otros datos'),
                blank=True,
                null=True)
    admin_resolucion = models.ForeignKey(Usuario,
                related_name='adm',
                blank=True,
                null=True, verbose_name=ugl(u'Usuario'))

    def __unicode__(self):
        return u'%s, %s' % (self.usuario_asoc, self.tipo)

    def resolucion_tag(self):
        return mark_safe(self.texto_resolucion)

    class Meta(object):
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class Comunicacion(models.Model):
    '''Es la clase de las incidencias generales'''
    comunidad_asoc = models.ForeignKey(Comunidad,
                related_name='com')
    propietario_asoc = models.ForeignKey(Usuario,
                related_name='prop')
    usuario_asoc = models.ForeignKey(Usuario,
                related_name='usrnm',
                blank=True,
                null=True)

    tipo = models.CharField(max_length=1,
                choices=tipo_comunicacion)
    estado = models.CharField(max_length=1,
                choices=tipo_ticket)

    fecha_creacion = models.DateTimeField(ugl(u'Fecha'))
    texto_creacion = models.TextField(ugl(u'Explicación'),
                default='...')

    fecha_resolucion = models.DateTimeField(ugl(u'Fecha'),
                blank=True, null=True)
    texto_resolucion = models.TextField(ugl(u'Otros datos'),
                blank=True, null=True)

    def __unicode__(self):
        return u'%s, %s' % (self.tipo, self.propietario_asoc)

    def resolucion_tag(self):
        return mark_safe(self.texto_resolucion)

    class Meta(object):
        verbose_name = u'Comunicación'
        verbose_name_plural = u'Comunicaciones'
