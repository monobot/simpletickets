# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class UserTicketPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class StaffTicketPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
