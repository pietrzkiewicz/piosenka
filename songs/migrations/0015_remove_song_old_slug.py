# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-29 12:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0014_auto_20180728_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='old_slug',
        ),
    ]
