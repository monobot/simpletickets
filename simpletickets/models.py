# -*- coding: utf-8 -*-
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as ugl
from django.conf import settings

from settings import (TICKET_ATTACHMENTS, DELTA_CLOSE, TICKET_TYPE,
        TICKET_SEVERITY, TICKET_STATE)

from simpleemail.email_helper import EmailManager


def uploadAttachment(instance, filename):
    return os.path.join(TICKET_ATTACHMENTS, filename)


class TicketManager(models.Manager):
    def n_solved(self):
        return len(Ticket.objects.filter(state__gt=7))

    def n_total(self):
        return len(Ticket.objects.all())

    def all(self):
        all_objects = super(TicketManager, self).all()
        for obj in all_objects:
            if obj.state == 8 and (
                    obj.resolution_date + DELTA_CLOSE <
                    timezone.now()):
                obj.state = 9
                obj.save()
        return all_objects


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

    resolution_delta = models.FloatField(_('delayed time in seconds'),
            blank=True, null=True)

    def resolucion_tag(self):
        return mark_safe(self.resolution_text)

    def humanized_delta(self):
        return self.resolution_date - self.creation_date

    def save(self, *args, **kwargs):
        self.modification_date = timezone.now()
        if self.state == 1:
            if self.staff:
                self.state = 2
        elif self.state > 7:
            self.resolution_date = timezone.now()
        if self.resolution_date:
            delta = self.resolution_date - self.creation_date
            self.resolution_delta = int(delta.total_seconds())
        super(Ticket, self).save(*args, **kwargs)
        # self._monitor()
        if not self.ticket_number:
            self.ticket_number = str(self.creation_date)[2:4] + (
                    '00000{id}'.format(id=self.id))[-6:]
            self.save()

        self._mailSender()

    def _mailSender(self):
        context = ''
        if self.state == 9:
            context = ('We are glad we have solved your ticket number: '
                    '{ticket_number}\n\n'
                    'The resolution time was {resolution_delta}.\n\n'
                    'You have {DELTA_CLOSE} hours to reopen it, '
                    'remember to carefully explain your reasons.\nThe Team'
                    ).format(
                            ticket_number=self.ticket_number,
                            resolution_delta=self.resolution_delta,
                            DELTA_CLOSE=DELTA_CLOSE,
                    )
            subject = ('Your ticket number {ticket_number} has been solved'
                    ).format(
                            ticket_number=self.ticket_number,
                    )
            body = ('Your {ticket_number} has been solved!').format(
                            ticket_number=self.ticket_number,
                    )
            email = self.user.email
            self.sendEmail(context, subject, body, email)
        if self.state == 2:
            context = ('You have been assigned ticket number {ticket_number}.'
                    '\n\nThe Team').format(
                            ticket_number=self.ticket_number,
                    )
            subject = ('You have been assigned ticket number {ticket_number}.'
                    '\n\nThe Team').format(
                            ticket_number=self.ticket_number,
                    )
            body = ('You have been assigned ticket number {ticket_number}.'
                    '\n\nThe Team').format(
                            ticket_number=self.ticket_number,
                    )
            email = self.staff.email
            self.sendEmail(context, subject, body, email)

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

    # def monitorfile(self):
    #     return os.path.join(settings.MEDIA_ROOT, 'simpletickets',
    #         '{id}-{user}-{date}.mon'.format(
    #                 id=self.id,
    #                 user=self.user,
    #                 date=self.creation_date.strftime('%y%m%d'),
    #             ))

    # def _monitor(self):
    #     with open(self.monitorfile()) as monitor:
    #         print monitor

    def __unicode__(self):
        return u'{ticket_number} {user}'.format(
                ticket_number=self.ticket_number,
                user=self.user,
                )

    class Meta(object):
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ('state', 'severity', 'creation_date')
