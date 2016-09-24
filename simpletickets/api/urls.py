# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from simpletickets.api.views import UserTicketListCreate  # noqa


urlpatterns = patterns(
    url(r'^list/$', UserTicketListCreate.as_view(), name='ticketListCreate'),
    )

urlpatterns = format_suffix_patterns(urlpatterns)
