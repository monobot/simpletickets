# -*- coding: utf-8 -*-
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as ugl
from django.conf import settings

from .settings import (ST_ATTACHMENTS, ST_DELTA_CLOSE,
    ST_TCKT_TYPE, ST_TCKT_SEVERITY, ST_TCKT_STATE,
    )
from .helpers import monitor, monitorfile, monitorfile_url

from .simpleemail.email_helper import EmailManager


def uploadAttachment(instance, filename):
    return os.path.join(ST_ATTACHMENTS, filename)


class TicketManager(models.Manager):
    def n_solved(self, user):
        return len(Ticket.objects.filter(state__gt=7, user=user))

    def n_total(self, user):
        return len(Ticket.objects.filter(user=user))

    def all(self):
        all_objects = super(TicketManager, self).all()

        # rewrite the all() method
        # so we can update files older than ST_DELTA_CLOSE to state 9
        now_minus_delta = timezone.now() - ST_DELTA_CLOSE
        state_8_delta = all_objects.filter(
            state=8,
            resolution_date__lt=now_minus_delta
            )
        state_8_delta.update(state=9)

        return all_objects


class Ticket(models.Model):
    objects = TicketManager()
    ticket_number = models.CharField(max_length=8, blank=True, null=True)

    user = models.ForeignKey(User,)
    staff = models.ForeignKey(User,
        limit_choices_to={'is_staff': True},
        related_name='usrStaff',
        blank=True, null=True,
        )

    ticket_type = models.IntegerField(default=2, choices=ST_TCKT_TYPE)
    severity = models.IntegerField(default=3, choices=ST_TCKT_SEVERITY)
    state = models.IntegerField(default=1, choices=ST_TCKT_STATE)

    description = models.TextField(ugl(u'Description'), default='...')
    attachment = models.FileField(upload_to=uploadAttachment,
        blank=True, null=True)

    resolution_text = models.TextField(ugl(u'Resolution text'), default='')

    creation_date = models.DateTimeField(_('Creation Date'),
        default=timezone.now)
    modification_date = models.DateTimeField(_('Last Modification Date'),
        blank=True, null=True)
    resolution_date = models.DateTimeField(_('Resolution date'),
        blank=True, null=True)

    resolution_delta = models.FloatField(_('delayed time in seconds'),
        blank=True, null=True)

    def mntrfile(self):
        return monitorfile_url(self)

    def resolucion_tag(self):
        return mark_safe(self.resolution_text)

    def humanized_delta(self):
        return self.resolution_date - self.creation_date

    def save(self, *args, **kwargs):
        self.modification_date = timezone.now()
        if self.id:
            header_msg = self.changesChecker(
                Ticket.objects.get(id=self.id),
                self
                )
        else:
            header_msg = _('{date} #### Ticket created ####\n').format(
                date=self.creation_date,
                )
        if self.state == 1:
            if self.staff:
                self.state = 2
        elif self.state > 7:
            self.resolution_date = timezone.now()
        if self.resolution_date:
            delta = self.resolution_date - self.creation_date
            self.resolution_delta = int(delta.total_seconds())
        super(Ticket, self).save(*args, **kwargs)
        monitor(monitorfile(self), header_msg)
        if not self.ticket_number:
            self.ticket_number = str(self.creation_date)[2:4] + (
                '00000{id}'.format(id=self.id)
                )[-6:]
            self.save()

    def _mailSender(self):
        context = ''
        if self.state == 9:
            context = {}
            subject = _(
                'Your ticket number {ticket_number} has been solved'
                ).format(ticket_number=self.ticket_number)
            body = _('We are glad we have solved your ticket number: '
                '{ticket_number}\n\n'
                'The resolution time was {resolution_delta}.\n\n'
                'You have {ST_DELTA_CLOSE} hours to reopen it, '
                'remember to carefully explain your reasons.\nThe Team'
                ).format(ticket_number=self.ticket_number,
                    resolution_delta=self.resolution_delta,
                    ST_DELTA_CLOSE=ST_DELTA_CLOSE
                    )
            email = self.user.email
            self.sendEmail(context, subject, body, email)
        if self.state == 2:
            context = {}
            subject = _(
                'Ticket {ticket_number} assigned.\n\nThe Team'
                ).format(ticket_number=self.ticket_number)
            body = _(
                'You have been assigned ticket number {ticket_number}.'
                '\n\nThe Team'
                ).format(ticket_number=self.ticket_number)
            email = self.staff.email
            self.sendEmail(context, subject, body, email)

    def changesChecker(self, original, actual):
        MONITORIZED = ['ticket_number', 'user', 'staff', 'ticket_type',
            'severity', 'state', 'description', 'resolution_text'
            ]
        msg = []
        for attribute in MONITORIZED:
            attr_ori = getattr(original, attribute)
            attr_act = getattr(actual, attribute)
            value = attr_act
            if attribute in ['ticket_type', 'severity', 'state']:
                value = getattr(actual, 'get_{attribute}_display'.format(
                    attribute=attribute)
                    )()
            if not attr_ori == attr_act and (attr_ori or attr_act):
                msg.append(
                    '[{attrname}: {attrvalue}]'.format(
                        attrname=attribute.upper(),
                        attrvalue=value,
                        )
                    )
        if msg:
            msg = ' | '.join(msg) + '\n'
        else:
            msg = 'No changes!\n'
        return msg

    def sendEmail(self, context, subject, body, email):
        EmailManager(context,
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=self.user.email,
            bcc=email,
            connection=None,
            attachments=None,
            headers=None,
            alternatives=None,
            cc=None,
            reply_to=None
            )

    def __unicode__(self):
        return u'{ticket_number} {user}'.format(
            ticket_number=self.ticket_number,
            user=self.user,
            )

    class Meta(object):
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ('state', 'severity', 'creation_date')
