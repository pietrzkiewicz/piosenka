# Generated by Django 2.1.15 on 2020-06-06 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0002_auto_20180812_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='has_extra_chords',
            field=models.BooleanField(blank=True, default=False, editable=False, help_text='True iff the lyrics contain repeated chords.'),
        ),
    ]