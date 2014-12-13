# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ready',
            field=models.BooleanField(editable=False, default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='reviewed',
            field=models.BooleanField(editable=False, default=False),
            preserve_default=True,
        ),
    ]
