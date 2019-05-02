# -*- coding: utf-8 -*-
## Author: Aziz Khan
## License: GPL v3
## Copyright © 2018 Aziz Khan <azez.khan__AT__gmail.com>

# Make sure the following:
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


#Model for Factor table in the database
class Factor(models.Model):
    data_source = (
        ('ENCODE', 'ENCODE'),
        ('GEO', 'GEO'),
        ('Array Express', 'AE')
        )
    tf_name = models.CharField(max_length=255)  
    data_source = models.CharField(max_length=16, blank=False, choices=data_source) 
    cell_line = models.CharField(max_length=255)
    biological_condition = models.CharField(max_length=255, blank=True)
    identifier = models.CharField(max_length=16)
    jaspar_id = models.CharField(max_length=16, blank=True) 
    jaspar_version = models.CharField(max_length=1, blank=True)
    folder = models.CharField(max_length=255, unique=True)
    total_peaks = models.CharField(max_length=16, blank=True) 

    def __str__(self):
        return self.tf_name

#Model for FactorData table in the database
class FactorData(models.Model):
    model_choices = (
        ('PWM', 'PWM'),
        ('DiMO','DiMO'),
        ('TFFM', 'TFFM'),
        ('DNAShaped_4bits', 'DNAShaped_4bits'),
        ('DNAShaped_pssm', 'DNAShaped_pssm'),
        ('DNAShaped_tffm', 'DNAShaped_tffm'),
        ('NRG', 'NRG')
    )

    peakcaller_choices = (
        ('MACS', 'MACS'),
        ('BCP', 'BCP'),
        ('HOMER', 'HOMER')
        )
    peak_caller = models.CharField(max_length=16, blank=False, choices=peakcaller_choices) 
    prediction_model = models.CharField(max_length=16, blank=False, choices=model_choices) 
    model_detail = models.CharField(blank=True, max_length=150)
    folder = models.ForeignKey(Factor, to_field='folder', db_column='folder', related_name='folders')
    jaspar_id = models.CharField(max_length=16, blank=True) 
    jaspar_version = models.CharField(max_length=1, blank=True)
    distance_threshold = models.CharField(max_length=16)
    score_threshold = models.CharField(max_length=16) 
    adj_centrimo_pvalue = models.CharField(max_length=16)
    total_tfbs = models.CharField(max_length=16, blank=True)
    

#Model for Post table in the database
class Post(models.Model):
    category_choices = (
        ('Update', 'Update'),
        ('Bug fix', 'Bug fix'),
        ('Announcement', 'Announcement'),
        ('Other', 'Other'),    
    )
    title = models.CharField(max_length=100)  
    content = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=150, choices=category_choices)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)


