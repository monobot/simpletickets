# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simpletickets', '0003_auto_20150828_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responseticket',
            name='asigned_to',
        ),
        migrations.RemoveField(
            model_name='responseticket',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='responseticket',
            name='ticket',
        ),
        migrations.AddField(
            model_name='ticket',
            name='resolution_text',
            field=models.TextField(default=b'', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='staff',
            field=models.ForeignKey(related_name='usrStaff', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='ResponseTicket',
        ),
    ]
