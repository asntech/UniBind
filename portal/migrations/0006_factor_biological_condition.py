# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-23 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_remove_factor_biological_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='biological_condition',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
