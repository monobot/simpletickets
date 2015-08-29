# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpletickets', '0004_auto_20150829_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='resolution_text',
            field=models.TextField(default=b'', verbose_name='Resolution text'),
        ),
    ]
