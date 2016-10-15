# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from simpletickets import urls as ticket_urls

from .views import Activate, Activation, ActivationCompleted, HomeView  # noqa

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tickets/', include(ticket_urls)),
    # USER VIEWS
    url(r'activate/$', Activate.as_view(),
            name='activate'),
    url(r'activation/$', Activation.as_view(),
            name='activation'),
    url(r'activation-completed/$', ActivationCompleted.as_view(),
            name='activationCompleted'),
    ]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        ]

urlpatterns += [
    # USER HELPFULL VIEWS
    url(r'login/$',
            'django.contrib.auth.views.login',
            {'template_name': 'user/login.html'},
                    name='login'),
    url(r'change-password/$',
            'django.contrib.auth.views.password_reset',
            {'template_name': 'user/password_reset_form.html'},
                    name='changepassword'),
    url(r'change-reset-done/$',
            'django.contrib.auth.views.password_reset_done',
            {'template_name': 'user/password_reset_done.html'},
                    name='password_reset_done'),
    url(r'password-change/confirmation-url/(?P<uidb64>[0-9A-Za-z_\-]+)/' +
            r'(?P<token>.+)/$',
            'django.contrib.auth.views.password_reset_confirm',
            {'template_name': 'user/password_reset_confirm.html'},
                    name='password_reset_confirm'),
    url(r'password-change/completed/$',
            'django.contrib.auth.views.password_reset_complete',
            {'template_name': 'user/password_reset_complete.html'},
                    name='password_reset_complete'),
    url(r'logout/$',
            'django.contrib.auth.views.logout',
            {'template_name': 'user/logout.html'},
                    name='logout'),
    ]
