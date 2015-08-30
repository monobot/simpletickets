# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpletickets', '0002_auto_20150830_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='state',
            field=models.IntegerField(default=1, choices=[(1, 'new'), (2, 'assigned'), (5, 'delayed'), (8, 'solved'), (9, 'closed')]),
        ),
    ]
