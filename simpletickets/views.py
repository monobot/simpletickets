# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from models import Ticket
from forms import TicketFormUser, TicketFormStaff
from settings import BASE_TEMPLATE


# MIXINS
class ContextMixin(SuccessMessageMixin, View):
    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['base_template'] = BASE_TEMPLATE
        context['objects'] = Ticket.objects
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
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs['ticket_id'])
# END MIXINS


class TicketCreate(ContextMixin, Login_required_mixin, CreateView):
    title = _('Edit ticket')
    model = Ticket
    fields = ['ticket_type', 'severity', 'description', 'attachment', ]
    success_message = _('ticket was successfully created')
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
    success_message = _('ticket was successfully deleted')
    success_url = reverse_lazy('ticketList')


class TicketUpdate(ContextMixin, Login_required_mixin, TicketMixin,
        UpdateView):
    title = _('Delete ticket')
    model = Ticket
    success_url = reverse_lazy('home')
    success_message = _('ticket was successfully updated')
    success_url = reverse_lazy('ticketList')

    def get_form_class(self):
        if self.request.user.is_staff:
            return TicketFormStaff
        return TicketFormUser

    def form_valid(self, form):
        ticket = form.instance
        if not ticket.staff and self.request.user.is_staff:
            ticket.staff = self.request.user
        return super(TicketUpdate, self).form_valid(form)


class TicketList(ContextMixin, Login_required_mixin, TicketMixin, ListView):
    model = Ticket
    title = _('Ticket list')
