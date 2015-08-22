# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import Ticket


# MIXINS
class ContextMixin(SuccessMessageMixin, View):
    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class Login_required_mixin(View):
    @classmethod
    def as_view(self, **kwargs):
        return login_required(
                super(Login_required_mixin, self).as_view(**kwargs)
                )
# END MIXINS


class TicketCreate(ContextMixin, Login_required_mixin,
        CreateView):
    model = Ticket
    title = _('Edit ticket')
    success_message = _("%(ticket_number)s was successfully updated")
    error_message = _("Please check the failures bellow")


class TicketUpdate(ContextMixin, Login_required_mixin,
        UpdateView):
    model = Ticket
    title = _('Edit ticket')
    success_message = _("%(ticket_number)s was successfully updated")
    error_message = _("Please check the failures bellow")


class TicketDelete(ContextMixin, Login_required_mixin,
        DeleteView):
    model = Ticket
    title = _('Delete ticket')
    success_url = reverse_lazy('home')
    success_message = _("%(ticket_number)s was successfully deleted")


class TicketList(ContextMixin, Login_required_mixin, ListView):
    model = Ticket
    title = _('Ticket list')

    def get_queryset(self):
        if self.request.user.is_staff():
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)
