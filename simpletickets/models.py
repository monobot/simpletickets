# -*- coding: utf-8 -*-
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as ugl

from settings import (TICKET_ATTACHMENTS, TICKET_TYPE, TICKET_SEVERITY,
        TICKET_STATE)


def uploadAttachment(instance, filename):
    return os.path.join(TICKET_ATTACHMENTS, filename)


class TicketManager(models.Manager):
    def n_open(self):
        return len(Ticket.objects.filter(state__lt=4))

    def n_solved(self):
        return len(Ticket.objects.filter(state=4))

    def n_total(self):
        return len(Ticket.objects.all())

    def fastest(self):
        return Ticket.objects.all()[0]


class Ticket(models.Model):
    objects = TicketManager()
    ticket_number = models.CharField(max_length=8,
                blank=True,
                null=True)

    user = models.ForeignKey(User,)
    staff = models.ForeignKey(User,
            limit_choices_to={'is_staff': True},
            related_name='usrStaff',
            blank=True, null=True,
            )

    ticket_type = models.IntegerField(default=2, choices=TICKET_TYPE)
    severity = models.IntegerField(default=3, choices=TICKET_SEVERITY)
    state = models.IntegerField(default=1, choices=TICKET_STATE)

    description = models.TextField(ugl(u'Description'),
            default='...')
    attachment = models.FileField(upload_to=uploadAttachment,
            blank=True, null=True)

    resolution_text = models.TextField(ugl(u'Resolution text'),
            default='')

    creation_date = models.DateTimeField(_('Creation Date'),
            default=timezone.now)
    modification_date = models.DateTimeField(_('Last Modification Date'),
            blank=True, null=True)
    resolution_date = models.DateTimeField(_('Resolution date'),
            blank=True, null=True)

    def resolution_delta(self):
        return self.resolution_date - self.creation_date

    def __unicode__(self):
        return u'%s, %s' % (self.user, self.ticket_type)

    def resolucion_tag(self):
        return mark_safe(self.resolution_text)

    def save(self, *args, **kwargs):
        self.modification_date = timezone.now()
        super(Ticket, self).save(*args, **kwargs)
        if not self.ticket_number:
            self.ticket_number = str(self.creation_date)[2:4] + (
                    '00000{id}'.format(id=self.id))[-6:]
            self.save()

    class Meta(object):
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ('state', 'severity', 'creation_date')
