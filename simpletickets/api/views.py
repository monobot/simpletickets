# -*- coding: utf-8 -*-
from django.db.models import Q

from rest_framework.generics import (ListCreateAPIView, ListAPIView,
    RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
    )  # noqa
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from simpletickets.api.permissions import (UserTicketPermission,
    StaffTicketPermission
    )  # noqa
from simpletickets.api.serializers import (UserTicketSerializer,
    StaffTicketSerializer
    )  # noqa
from simpletickets.models import Ticket


class Custom20Pagination(PageNumberPagination):
    '''
    A pagination class that paginates every 20 objects.
    '''
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
                'links': {'next': self.get_next_link(),
                   'previous': self.get_previous_link()
                    },
                'count': self.page.paginator.count,
                'results': data
                }
            )


class MainMixin(object):
    '''
    The main mixin for all the views,
    where we manage the methods that are used more than once.
    '''
    def logged_user(self):
        '''
        Returns the user that is logged,
        '''
        return self.request.user


class UserTicketMixin(MainMixin):
    permission_classes = (UserTicketPermission, )
    serializer_class = UserTicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.logged_user())

    def perform_create(self, serializer):
        user = self.logged_user()
        serializer.save(user=user)


class UserTicketListCreate(UserTicketMixin, ListCreateAPIView):
    '''
    GET list of tickets in the database for the logged in user
    CREATE a ticket for the logged in user
    '''
    pass


class UserTicketUpdateDelete(UserTicketMixin, RetrieveUpdateDestroyAPIView):
    pass


class StaffTicketMixin(MainMixin):
    permission_classes = (StaffTicketPermission, )
    serializer_class = StaffTicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(
            Q(state=1) |
            Q(staff=self.request.user, state__lt=9)
            )

    def perform_create(self, serializer):
        user = self.logged_user()
        serializer.save(staff=user)


class StaffTicketList(StaffTicketMixin, ListAPIView):
    '''
    GET list of tickets in the database for the logged in staff member
    that is all the tickets assigned and all unassigned tickets
    '''
    pass


class StaffTicketUpdate(StaffTicketMixin, RetrieveUpdateAPIView):
    pass
