# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simpletickets', '0002_ticket_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('modification_date', models.DateTimeField(null=True, verbose_name='Last Modification Date', blank=True)),
                ('resolution_date', models.DateTimeField(null=True, verbose_name='Resolution date', blank=True)),
                ('ticket_type', models.IntegerField(default=2, choices=[(1, 'Inform about an error'), (2, 'Problem'), (3, 'Propose a sugestion'), (4, 'Others')])),
                ('severity', models.IntegerField(default=3, choices=[(1, 'Critical'), (2, 'Very important'), (3, 'Important'), (4, 'Normal')])),
                ('state', models.IntegerField(default=1, choices=[(1, 'new'), (2, 'assigned'), (3, 'solved'), (4, 'closed')])),
                ('resolution_text', models.TextField(default=b'', verbose_name='Description')),
                ('asigned_to', models.ForeignKey(related_name='assigned', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('staff', models.ForeignKey(related_name='usrStaff', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('state', 'severity', 'creation_date'),
                'verbose_name': 'Response Ticket',
                'verbose_name_plural': 'Response Tickets',
            },
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='resolution_text',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticket',
        ),
        migrations.AddField(
            model_name='ticket',
            name='modification_date',
            field=models.DateTimeField(null=True, verbose_name='Last Modification Date', blank=True),
        ),
        migrations.AddField(
            model_name='responseticket',
            name='ticket',
            field=models.ForeignKey(to='simpletickets.Ticket'),
        ),
    ]
