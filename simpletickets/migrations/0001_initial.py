# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import simpletickets.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_number', models.CharField(max_length=8, null=True, blank=True)),
                ('ticket_type', models.IntegerField(default=2, choices=[(1, 'Inform about an error'), (2, 'Problem'), (3, 'Propose a sugestion'), (4, 'Others')])),
                ('severity', models.IntegerField(default=3, choices=[(1, 'Critical'), (2, 'Very important'), (3, 'Important'), (4, 'Normal')])),
                ('state', models.IntegerField(default=1, choices=[(1, 'new'), (2, 'assigned'), (3, 'solved'), (4, 'closed')])),
                ('description', models.TextField(default=b'...', verbose_name='Description')),
                ('attachment', models.FileField(null=True, upload_to=simpletickets.models.uploadAttachment, blank=True)),
                ('resolution_text', models.TextField(default=b'', verbose_name='Resolution text')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('modification_date', models.DateTimeField(null=True, verbose_name='Last Modification Date', blank=True)),
                ('resolution_date', models.DateTimeField(null=True, verbose_name='Resolution date', blank=True)),
                ('resolution_delta', models.FloatField(null=True, verbose_name='delayed time in seconds', blank=True)),
                ('staff', models.ForeignKey(related_name='usrStaff', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('state', 'severity', 'creation_date'),
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
    ]
