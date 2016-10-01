# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Ticket  # noqa
from .forms import TicketFormUser, TicketFormStaff
from .helpers import monitor, monitorfile
from .settings import (BASE_TEMPLATE, ST_FL_MNTR_OWNER, ST_FL_MNTR_STAFF,
    ST_SETT_NUMBERS_STAFF, ST_SETT_NUMBERS_OWNER, ST_SETT_TIMES_STAFF,
    ST_SETT_TIMES_OWNER, ST_SETT_MAIN_TASKBAR, ST_STAFF_GNAME, ST_ADMIN_GNAME
    )


# MIXINS
class ContextMixin(SuccessMessageMixin, View):
    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['base_template'] = BASE_TEMPLATE

        is_staff = self.request.user.is_staff
        context['ST_MNTR'] = is_staff and ST_FL_MNTR_STAFF or ST_FL_MNTR_OWNER
        stt_numb = is_staff and ST_SETT_NUMBERS_STAFF or ST_SETT_NUMBERS_OWNER
        stt_times = is_staff and ST_SETT_TIMES_STAFF or ST_SETT_TIMES_OWNER

        context['ST_SETT_MAIN_TASKBAR'] = ST_SETT_MAIN_TASKBAR

        if stt_numb:
            context['stt_numb'] = stt_numb
            n_solved = Ticket.objects.n_solved(self.request.user)
            n_total = Ticket.objects.n_total(self.request.user)
            if n_solved and n_total:
                context['porc_solved'] = n_solved * 100 / n_total
                context['porc_pending'] = 100 - context['porc_solved']
            elif n_total:
                context['porc_solved'] = 0
                context['porc_pending'] = 100
            else:
                context['porc_solved'] = 100
                context['porc_pending'] = 0
        if stt_times:
            context['statistic_times'] = stt_times
            all_tickets = Ticket.objects.all()
            if all_tickets.filter(state__gt=7):
                context['fastest'] = all_tickets.filter(state__gt=7
                    ).order_by('resolution_delta'
                    )[0].humanized_delta()
                if n_solved:
                    context['media'] = timedelta(
                        seconds=sum(
                            [t.resolution_delta for t in all_tickets.filter(
                                    state__gt=7)]) / n_solved
                        )
                else:
                    context['media'] = 'N/A'

        return context


class Login_required_mixin(View):
    @classmethod
    def as_view(self, **kwargs):
        return login_required(
            super(Login_required_mixin, self).as_view(**kwargs)
            )


class TicketMixin(object):
    staff_group = Group.objects.get_or_create(name=ST_STAFF_GNAME)[0]
    admin_group = Group.objects.get_or_create(name=ST_ADMIN_GNAME)[0]

    def get_queryset(self):
        user = self.request.user
        is_ticket_manager = user.groups.filter(
            name=self.staff_group.name
            ).exists()
        is_ticket_admin = user.groups.filter(
            name=self.admin_group.name
            ).exists()

        if is_ticket_admin:
            return Ticket.objects.filter(
                Q(state=1) |
                Q(state__lt=9)
                )
        elif is_ticket_manager:
            return Ticket.objects.filter(
                Q(state=1) |
                Q(staff=user, state__lt=9)
                )
        return Ticket.objects.filter(user=user)

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs['ST_id'])
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
        header_msg = _('{date} [user: {user}] ').format(date=date, user=user)
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
