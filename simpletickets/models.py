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


class TimeStamper(models.Model):
    creation_date = models.DateTimeField(_('Creation Date'),
            default=timezone.now)
    modification_date = models.DateTimeField(_('Last Modification Date'),
            blank=True, null=True)
    resolution_date = models.DateTimeField(_('Resolution date'),
            blank=True, null=True)

    def resolution_delta(self):
        return self.resolution_date - self.creation_date

    def save(self, *args, **kwargs):
        self.modification_date = timezone.now()
        super(TimeStamper, self).save(*args, **kwargs)

    class Meta(object):
        abstract = True


class Ticket(TimeStamper):
    user = models.ForeignKey(User,)

    ticket_number = models.CharField(max_length=8,
                blank=True,
                null=True)

    ticket_type = models.IntegerField(default=2, choices=TICKET_TYPE)

    severity = models.IntegerField(default=3, choices=TICKET_SEVERITY)

    state = models.IntegerField(default=1, choices=TICKET_STATE)

    description = models.TextField(ugl(u'Description'),
            default='...')
    attachment = models.FileField(upload_to=uploadAttachment,
            blank=True, null=True)

    def __unicode__(self):
        return u'%s, %s' % (self.user, self.ticket_type)

    def resolucion_tag(self):
        return mark_safe(self.resolution_text)

    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)
        if not self.ticket_number:
            self.ticket_number = str(self.creation_date)[2:4] + (
                    '00000{id}'.format(id=self.id))[-6:]
            self.save()

    def get_responses(self):
        return self.responseticket_set.all()

    def last_response(self):
        return self.responseticket_set.all()[0]

    class Meta(object):
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ('state', 'severity', 'creation_date')


class ResponseTicket(TimeStamper):
    ticket = models.ForeignKey(Ticket)

    staff = models.ForeignKey(User,
            limit_choices_to={'is_staff': True},
            related_name='usrStaff',
            blank=True, null=True,
            )

    asigned_to = models.ForeignKey(User,
            limit_choices_to={'is_staff': True},
            related_name='assigned',
            blank=True, null=True,
            )

    ticket_type = models.IntegerField(default=2, choices=TICKET_TYPE)
    severity = models.IntegerField(default=3, choices=TICKET_SEVERITY)
    state = models.IntegerField(default=2, choices=TICKET_STATE)

    resolution_text = models.TextField(ugl(u'Description'),
            default='')

    def save(self, *args, **kwargs):
        self.ticket.ticket_type = self.ticket_type
        self.ticket.severity = self.severity
        self.ticket.state = self.state
        if self.state > 2:
            now = timezone.now()
            self.resolution_date = now
            self.ticket.resolution_date = now
        self.ticket.save()

        super(ResponseTicket, self).save(*args, **kwargs)

    class Meta(object):
        verbose_name = 'Response Ticket'
        verbose_name_plural = 'Response Tickets'
        ordering = ('state', 'severity', 'creation_date')
