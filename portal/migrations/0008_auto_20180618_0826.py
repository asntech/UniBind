# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-18 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20180501_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='jaspar_id',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='jaspar_version',
        ),
        migrations.AddField(
            model_name='factordata',
            name='jaspar_id',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name='factordata',
            name='jaspar_version',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
