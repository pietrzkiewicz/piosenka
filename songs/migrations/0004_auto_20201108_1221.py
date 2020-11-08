# Generated by Django 3.0.7 on 2020-11-08 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_auto_20200606_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, '(deprecated) Wykonawca własnych tekstów'), (2, '(deprecated) Kompozytor'), (3, 'Twórca zagraniczny'), (4, '(deprecated) Zespół'), (5, 'Twórca polski'), (6, 'Środowisko')], help_text='Kategoria w spisie treści śpiewnika.', null=True),
        ),
    ]
