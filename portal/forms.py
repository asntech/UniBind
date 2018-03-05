# -*- coding: utf-8 -*-
## Author: Aziz Khan
## License: GPL v3
## Copyright © 2017 Aziz Khan <azez.khan__AT__gmail.com>

from django import forms
from .models import Factor, FactorData

class ContactForm(forms.Form):
    '''
	Form for contact us page
    '''
    #from_name = forms.CharField(label='Your name', required=True, max_length=100)
    from_email = forms.EmailField(required=True, label='Your email')
    subject = forms.CharField(label='Subject', required=False, max_length=100)
    message = forms.CharField(label='Your message/feedback', required=True, widget=forms.Textarea)


class SearchForm(forms.Form):
	
	'''
	Form for advanced search options
    '''
    #tf_name
	tf_name = forms.CharField(widget=forms.Select(
    	choices=Factor.objects.all().values('tf_name').distinct().values_list('tf_name', 'tf_name')
    	))

	#TF Class
	prediction_model = forms.CharField(
    	widget=forms.Select(
    		choices = FactorData.objects.all().values('prediction_model').distinct().values_list('prediction_model', 'prediction_model')
			)
		) 

	#cell_line
	cell_line = forms.CharField(
		widget=forms.Select(
			choices = Factor.objects.all().values('cell_line').distinct().values_list('cell_line', 'cell_line')
			)
		)