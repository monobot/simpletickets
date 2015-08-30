# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpletickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='state',
            field=models.CharField(default=b'new', max_length=15, choices=[(b'new', 'new'), (b'assigned', 'assigned'), (b'solved', 'solved'), (b'closed', 'closed')]),
        ),
    ]
