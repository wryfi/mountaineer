# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0009_auto_20171111_0444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='cpu_count',
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_manufacturer',
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_model',
        ),
        migrations.AddField(
            model_name='server',
            name='cores',
            field=models.PositiveIntegerField(blank=True, help_text='Number of CPU cores', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='memory',
            field=models.PositiveIntegerField(blank=True, help_text='Physical RAM in MiB', null=True),
        ),
    ]