# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from models import Ticket
from forms import TicketFormUser, TicketFormStaff
from settings import (BASE_TEMPLATE, TICKET_MNTR_OWNER, TICKET_MNTR_STAFF,
        STATISTIC_NUMBERS_STAFF, STATISTIC_NUMBERS_OWNER,
        STATISTIC_TIMES_STAFF, STATISTIC_TIMES_OWNER)
from helpers import monitor, monitorfile


# MIXINS
class ContextMixin(SuccessMessageMixin, View):
    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['base_template'] = BASE_TEMPLATE

        if self.request.user.is_staff:
            context['ticket_mntr'] = TICKET_MNTR_STAFF
            statistic_numbers = STATISTIC_NUMBERS_STAFF
            statistic_times = STATISTIC_TIMES_STAFF
        else:
            context['ticket_mntr'] = TICKET_MNTR_OWNER
            statistic_numbers = STATISTIC_NUMBERS_OWNER
            statistic_times = STATISTIC_TIMES_OWNER

        if statistic_numbers:
            context['statistic_numbers'] = statistic_numbers
            n_solved = Ticket.objects.n_solved()
            n_total = Ticket.objects.n_total()
            if n_solved and n_total:
                context['porc_solved'] = n_solved * 100 / n_total
                context['porc_pending'] = 100 - context['porc_solved']
            elif n_total:
                context['porc_solved'] = 0
                context['porc_pending'] = 100
            else:
                context['porc_solved'] = 100
                context['porc_pending'] = 0
        if statistic_times:
            context['statistic_times'] = statistic_times
            all_tickets = Ticket.objects.all()
            if all_tickets.filter(state__gt=7):
                context['fastest'] = all_tickets.filter(state__gt=7
                        ).order_by('resolution_delta'
                    )[0].humanized_delta()
                context['media'] = timedelta(seconds=sum(
                        [t.resolution_delta for t in all_tickets.filter(
                                state__gt=7)]) / n_solved
                    )
        return context


class Login_required_mixin(View):
    @classmethod
    def as_view(self, **kwargs):
        return login_required(
                super(Login_required_mixin, self).as_view(**kwargs)
            )


class TicketMixin(object):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.filter(
                    Q(state=1) |
                    Q(staff=self.request.user, state__lt=9)
                )
        return Ticket.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs['ticket_id'])
# END MIXINS


class TicketCreate(ContextMixin, Login_required_mixin, CreateView):
    title = _('Edit ticket')
    model = Ticket
    fields = ['ticket_type', 'severity', 'description', 'attachment', ]
    success_message = _('Ticket was successfully created')
    error_message = _('Please check the failures bellow')
    success_url = reverse_lazy('ticketList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TicketCreate, self).form_valid(form)


class TicketDelete(ContextMixin, Login_required_mixin, TicketMixin,
        DeleteView):
    title = _('Delete ticket')
    model = Ticket
    success_url = reverse_lazy('home')
    success_message = _('Ticket was successfully deleted')
    success_url = reverse_lazy('ticketList')


class TicketUpdate(ContextMixin, Login_required_mixin, TicketMixin,
        UpdateView):
    title = _('Edit ticket')
    model = Ticket
    success_url = reverse_lazy('home')
    success_message = _('Ticket was successfully updated')
    success_url = reverse_lazy('ticketList')

    def getHeader(self, date, user):
        header_msg = _('** {date} [{user}]: ').format(
                date=date,
                user=user,
            )
        return header_msg

    def get_form_class(self):
        if self.request.user.is_staff:
            return TicketFormStaff
        return TicketFormUser

    def form_valid(self, form):
        ticket = form.instance
        header_msg = self.getHeader(
                ticket.creation_date,
                self.request.user.username
            )
        if not ticket.staff and self.request.user.is_staff:
            ticket.staff = self.request.user
        if not self.request.user.is_staff and ticket.state == 8:
            ticket.state = 2
            ticket.resolution_date = None
            ticket.resolution_delta = None

        monitor(monitorfile(ticket), header_msg)
        return super(TicketUpdate, self).form_valid(form)


class TicketList(ContextMixin, Login_required_mixin, TicketMixin, ListView):
    model = Ticket
    title = _('Ticket list')
