# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from simpletickets.settings.ticketSettings import (
    ST_STAFF_GNAME, ST_ADMIN_GNAME)


class Command(BaseCommand):
    help = '''Command that creates the module groups'''

    def handle(self, *args, **options):
        Group.objects.get_or_create(name=ST_STAFF_GNAME)

        Group.objects.get_or_create(name=ST_ADMIN_GNAME)
