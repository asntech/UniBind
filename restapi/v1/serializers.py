# -*- coding: utf-8 -*-
## Author: Aziz Khan
## License: GPL v3
## Copyright © 2017 Aziz Khan <azez.khan__AT__gmail.com>

from rest_framework import serializers
from portal.models import Factor, FactorData
from rest_framework.response import Response

from django.http import HttpRequest


class FactorDataSerializer(serializers.HyperlinkedModelSerializer):
    
    #bed_url = serializers.SerializerMethodField()

    class Meta:
        model = FactorData
        fields = ('peak_caller','model_detail','distance_threshold','score_threshold','adj_centrimo_pvalue','total_tfbs',)

    def get_bed_url(self, obj):
    	host_name = self.context['request'].build_absolute_uri(location='/')
    	return  str(host_name)+'static/data/macs/'+obj.prediction_model+'/'+obj.folder+'/' 

class FactorSerializer(serializers.HyperlinkedModelSerializer):

	#matrixannotations = MatrixAnnotationSerializer(many=True, read_only=True)
		
	jaspar_id = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	prediction_models = serializers.SerializerMethodField()
	pwm = serializers.SerializerMethodField()
	tffm = serializers.SerializerMethodField()
	dnashaped = serializers.SerializerMethodField()
	bem = serializers.SerializerMethodField()

	#url = serializers.HyperlinkedIdentityField(view_name='tf-detail', lookup_field='folder')
  	
	class Meta:
		model = Factor
		#fields = ('__all__')
		fields = ('tf_name', 'cell_line','biological_condition','data_source','jaspar_id','total_peaks','url','prediction_models','pwm','tffm','dnashaped','bem')
		ordering = ['tf_name','cell_line','total_peaks']



	def get_jaspar_id(self, obj):

		return obj.jaspar_id+'.'+str(obj.jaspar_version)

	def get_prediction_models(self, obj):
		return ['pwm','dnashaped','tffm','bem']

	def get_url(self, obj):

		host_name = self.context['request'].build_absolute_uri(location='/')
		
		return  str(host_name)+'api/v1/datasets/'+obj.folder+'/'

	def get_pwm(self, obj):
		return FactorDataSerializer(obj.folders.filter(prediction_model='DiMO'), many=True).data[0]

	def get_tffm(self, obj):
		return FactorDataSerializer(obj.folders.filter(prediction_model='TFFM'), many=True).data[0]

	def get_dnashaped(self, obj):
		return FactorDataSerializer(obj.folders.filter(prediction_model='DNAshaped'), many=True).data[0]

	def get_bem(self, obj):
		return FactorDataSerializer(obj.folders.filter(prediction_model='BEM'), many=True).data[0]


