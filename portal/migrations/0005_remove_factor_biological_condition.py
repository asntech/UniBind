# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-23 07:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_remove_factordata_model_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='biological_condition',
        ),
    ]
