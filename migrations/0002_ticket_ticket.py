# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpletickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket',
            field=models.ForeignKey(related_name='masterticket', blank=True, to='simpletickets.Ticket', null=True),
        ),
    ]
