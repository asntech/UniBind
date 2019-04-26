# -*- coding: utf-8 -*-
## Author: Aziz Khan
## License: GPL v3
## Copyright © 2017 Aziz Khan <azez.khan__AT__gmail.com>

from rest_framework import serializers
from portal.models import Factor, FactorData

from django.http import HttpRequest


class FactorDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FactorData
        fields = ('__all__')

class FactorSerializer(serializers.HyperlinkedModelSerializer):

	#matrixannotations = MatrixAnnotationSerializer(many=True, read_only=True)
		
	jaspar_id = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()

	#url = serializers.HyperlinkedIdentityField(view_name='matrix-detail', lookup_field='id')
  	
	class Meta:
		model = Factor
		#fields = ('__all__')
		fields = ('tf_name', 'cell_line','biological_condition','data_source','jaspar_id','total_peaks','url')
		ordering = ['tf_name']


	def get_jaspar_id(self, obj):

		return obj.jaspar_id+'.'+str(obj.jaspar_version)


	def get_url(self, obj):

		host_name = self.context['request'].build_absolute_uri(location='/')
		
		return  str(host_name)+'api/v1/tfs/'+obj.folder+'/'


