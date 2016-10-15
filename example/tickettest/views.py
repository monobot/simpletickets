# -*- coding: utf-8 -*-
from hashlib import md5

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import View


class HomeView(TemplateView):
    template_name = 'index.html'


def decoder(email, nombreuser, codigo):
    if md5('hola %s, %s' % (nombreuser, email)).hexdigest() == codigo:
        return True
    return False


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


# user activation and management
def activateUser(username, code):
    '''
    activates the user and confirmates the email address since this link
    is only known by the email owner
    '''
    user = User.objects.get(username=username)

    if decoder(user.email, user.username, code):
        user.is_active = True
        user.save()
        return user
    return False


class Activate(ContextMixin, TemplateView):
    title = _('Account Active')
    template_name = 'user/account_active.html'

    def get(self, request):
        user = activateUser(request.GET.get('user'),
                request.GET.get('code'))
        if user:
            return redirect('activationCompleted')
        else:
            raise Http404


class ActivationCompleted(ContextMixin, TemplateView):
    title = _('Registration completed')
    template_name = 'user/activation_completed.html'


class Activation(ContextMixin, TemplateView):
    title = 'Account Activation'
    template_name = 'user/activation.html'
