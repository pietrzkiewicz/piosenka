# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20141221_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='published',
        ),
    ]
