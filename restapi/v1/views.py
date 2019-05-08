# -*- coding: utf-8 -*-
## Author: Aziz Khan
## License: GPL v3
## Copyright © 2017 Aziz Khan <azez.khan__AT__gmail.com>
import os
from unibind.settings import BASE_DIR
from portal.models import Factor, FactorData
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from django.db.models import Q, Max
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.throttling import UserRateThrottle
from rest_framework import renderers

from rest_framework_jsonp.renderers import JSONPRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework_yaml.parsers import YAMLParser

from rest_framework.response import Response
from .serializers import FactorSerializer, FactorDataSerializer
import itertools

from rest_framework.pagination import (
    PageNumberPagination,
    )
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView, 
    )
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
    BaseFilterBackend,
    #DjangoFilterBackend,
    )

from django_filters.rest_framework import (
    DjangoFilterBackend,
    )

import coreapi
import coreschema
#from drf_openapi.utils import view_config

class FactorResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500


def _get_tfbs_url(request, factor_id, model_name,jaspar_id,jaspar_version, file_extension, model_detail=""):
    hostname = request.build_absolute_uri(location='/')
    if model_name == 'PWM':
        model_name = 'DiMO'
    if model_name == 'DNAshaped':
        model_detail = model_name+model_detail
    else:
        model_detail = model_name.lower()
    return  str(hostname)+'static/data/macs/'+model_name+'/'+factor_id+'/'+factor_id+'.'+jaspar_id+'.'+jaspar_version+'.'+model_detail+'.'+file_extension

def _get_peaks_url(request, factor_id):
    return  str(request.build_absolute_uri(location='/'))+'static/data/peaks/macs/'+factor_id+'/'+factor_id+'.narrowPeak'


def _get_cellline_url(request, cell_line):
    host_name = request.build_absolute_uri(location='/')
    return  str(host_name)+'api/v1/datasets?cell_line='+cell_line

def _get_tf_url(request, tf_name):
    host_name = request.build_absolute_uri(location='/')
    return  str(host_name)+'api/v1/datasets?tf_name='+tf_name



class BEDListRenderer(renderers.BaseRenderer):
    '''
    Render a list of sites in BED format.
    '''
    media_type = 'text/bed'
    format = 'bed'

    def render(self, data, media_type=None, renderer_context=None):

        bed = []
        import json
        for site in data['sites']:
            region = '\t'.join([site.get('chrom'), str(site.get('start')), site.get('end'), site.get('name'), '.', site.get('strand')+"\n"])
            bed.append(region)
        
        if not bed:
            bed = 'No BED available'
            return bed
        else:
            return bed


class TranscriptionFactorDetailsViewSet(APIView):
    """
    API endpoint that returns the tfbs detail information.
    """

    parser_classes = (YAMLParser,)
    renderer_classes = [renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    #@view_config(response_serializer=MatrixSerializer)
    def get(self, request, tf_id, format=None):
        """
        Gets tfbs detail information
        """

        setattr(request, 'view', 'api-browsable')

        
        data_dict = {}


        factor = Factor.objects.get(folder=tf_id)
        #factor = Factor.objects.values().get(folder=factor_id)

        dataqueryset = FactorData.objects.filter(folder=tf_id)

        #for dataqueryset in FactorData.objects.filter(folder=tf_id):
        #    dataqueryset.tfbs_url = "unibind/"

        factordata = FactorData.objects.values().filter(folder=tf_id)

        data_dict = {
                'tf_name': factor.tf_name,
                "cell_line": factor.cell_line,
                "biological_condition": factor.biological_condition,
                "identifier": factor.identifier,
                'jaspar_id': factor.jaspar_id+'.'+str(factor.jaspar_version),
                "tf_id": factor.folder,
                "total_peaks": factor.total_peaks,
                'peaks_url': _get_peaks_url(request, tf_id),
            }
        
        prediction_models = ['PWM','DNAshaped','TFFM','BEM']

        data_dict.update({'prediction_models': prediction_models})

        tfbs = []
        for model_name in factordata.values_list('prediction_model', flat=True).distinct():
            tfbs_list = []
            for i in list(dataqueryset.values('model_detail','total_tfbs','score_threshold','distance_threshold','adj_centrimo_pvalue','jaspar_id','jaspar_version').filter(folder=tf_id, prediction_model=model_name)):
                i.update(bed_url=_get_tfbs_url(request, tf_id, 'DNAshaped',i['jaspar_id'],i['jaspar_version'], 'bed', i['model_detail']),
                    fasta_url=_get_tfbs_url(request, tf_id, 'DNAshaped',i['jaspar_id'],i['jaspar_version'], 'fa', i['model_detail']),
                    summary_plot_url=_get_tfbs_url(request, tf_id, 'DNAshaped', i['jaspar_id'], i['jaspar_version'], 'png',i['model_detail']))
                tfbs_list.append(i)

            tfbs.append({model_name: tfbs_list})

        data_dict.update({'tfbs': tfbs})
        
        #data_dict.update({'tfbs': factordata})

    	#serializer = MatrixSerializer(matrix, context={'request': request})
        
        return Response(data_dict)


class UniBindFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='tf_name',
            location='query',
            schema=coreschema.String(
                description= 'Search by TF name (case-sensitive). For example: SMAD3',
                title= 'TF Name',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='cell_line',
            location='query',
            schema=coreschema.String(
                description= 'Cell line or tissue name. For example: MCF7',
                title= 'Cell line',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='biological_condition',
            location='query',
            schema=coreschema.String(
                description= 'Biological condition or source (e.g. dht).',
                title= 'Biological condition',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='identifier',
            location='query',
            schema=coreschema.String(
                description= 'The dataset identifier, such ENCODE or GEO dataset ID. For example: GSE60130',
                title= 'Identifier',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='data_source',
            location='query',
            schema=coreschema.String(
                description= 'Source of the data, such as ENCODE, GEO, AE(Array Express)',
                title= 'Data source',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='jaspar_id',
            location='query',
            schema=coreschema.String(
                description= 'JASPAR database profile matrix ID. For example: MA0492.1',
                title= 'JASPAR ID',
                ),
            required=False,
            type='string')
        ]

    def filter_queryset(self, request, queryset, view):

        query_string = request.GET.get('search', None)
        tf_name = request.GET.get('tf_name', None)
        cell_line = request.GET.get('cell_line', None)
        biological_condition = request.GET.get('biological_condition', None)
        identifier = request.GET.get('identifier', None)
        jaspar_id = request.GET.get('jaspar_id', None)
        data_source = request.GET.get('data_source', None)

        #if tf_name is set then filter queryset
        if tf_name and tf_name !='':
            queryset = queryset.filter(tf_name__iexact=tf_name)

        #if cell_line is set then filter queryset
        if cell_line and cell_line !='':
            queryset = queryset.filter(cell_line__iexact=cell_line)

        #if biological_condition is set then filter queryset
        if biological_condition and biological_condition !='':
            queryset = queryset.filter(biological_condition__iexact=biological_condition)

        #if identifier is set then filter queryset
        if identifier and identifier !='':
            queryset = queryset.filter(identifier__iexact=identifier)

        #if jaspar_id is set then filter queryset
        if jaspar_id and jaspar_id !='':
            jaspar_id = str(jaspar_id).split('.')[0]
            queryset = queryset.filter(jaspar_id__iexact=jaspar_id)

        #if data_source is set then filter queryset
        if data_source and data_source !='':
            queryset = queryset.filter(data_source__iexact=data_source)


        return queryset.order_by('tf_name')

class TranscriptionFactorsListViewSet(ListAPIView):
    """
    API endpoint that returns a list of all transcription factors.
    """

    queryset = Factor.objects.values_list('tf_name', flat=True).distinct()
    throttle_classes = (UserRateThrottle,)
    parser_classes = (YAMLParser,)
    renderer_classes = [renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    def get(self, request, format=None):
      """
      List all the transcription factors available in UniBind.
      """
      setattr(self.request, 'view', 'api-browsable')

      queryset = Factor.objects.values_list('tf_name', flat=True).distinct()
      
      data_dict = { 'count': queryset.count() }
      results = []
      for tf_name in queryset:
        results.append({
        'tf_name': tf_name,
        'url': _get_tf_url(request, tf_name)
        })

      data_dict.update({'results': results})

      return Response(data_dict)


class DatasetsListViewSet(ListAPIView):
    """
    REST API endpoint that returns a list of all the datasets used.
    """   
    serializer_class = FactorSerializer
    pagination_class = FactorResultsSetPagination
    throttle_classes = (UserRateThrottle,)
    filter_backends = [SearchFilter, OrderingFilter, UniBindFilterBackend]
    search_fileds = ['tf_name', 'cell_line','biological_condition','identifier','jaspar_id']
    filter_fileds = ['tf_name', 'cell_line','biological_condition','identifier','jaspar_id']
    parser_classes = (YAMLParser,)
    renderer_classes = [ renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    def get_queryset(self):
        """
        List all Datasets
        """

        setattr(self.request, 'view', 'api-browsable')
        queryset = Factor.objects.all().order_by('tf_name')

        return queryset


class CellTypesListViewSet(ListAPIView):
    """
    API endpoint that returns a list of all cell-lines/tissue names.
    """
    queryset = Factor.objects.values_list('cell_line', flat=True).distinct()
    filter_backends = [SearchFilter,]
    throttle_classes = (UserRateThrottle,)
    search_fileds = ['folder','tf_name','cell_line','biological_condition','data_source',]
    filter_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source',]
    parser_classes = (YAMLParser,)
    renderer_classes = [renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    def get(self, request):
      """
      List all the cell-lines/tissue names available in UniBind.
      """
      setattr(self.request, 'view', 'api-browsable')

      queryset = Factor.objects.values_list('cell_line', flat=True).distinct()
      
      data_dict = { 'count': queryset.count() }
      results = []
      for cell_line in queryset:
        results.append({
        'name': cell_line,
        'url': _get_cellline_url(self.request, cell_line)
        })

      data_dict.update({'results': results})

      return Response(data_dict)

    #def get_serializer_class(self):


# class CelllineFactorListViewSet(ListAPIView):
#     """
#     REST API endpoint that returns a list of all the transcription factors.
#     """
    
#     serializer_class = FactorSerializer
#     pagination_class = FactorResultsSetPagination
#     throttle_classes = (UserRateThrottle,)
#     filter_backends = [SearchFilter, OrderingFilter, ]
#     search_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
#     filter_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
#     parser_classes = (YAMLParser,)
#     renderer_classes = [ renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

#     def get(self, request, cell_line, format=None):
#         """
#         List all TFs in cell-lines
#         """

#         setattr(self.request, 'view', 'api-browsable')

#         queryset = Factor.objects.all().order_by('tf_name')

#         #cell_line = self.kwargs['cell_line']

#         #if tax group is set then filter queryset
#         if cell_line and cell_line !='':
#             queryset = queryset.values_list().filter(cell_line=cell_line).order_by('tf_name')
#         else:
#             queryset = None

#         return Response(queryset)



class APIRoot(APIView):
    """
    This is the root of the UniBind RESTful API v1. Please read the documentation for more details.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=format):
        setattr(request, 'view', 'api-browsable')
        return Response({
            'tfs': reverse('v1:tf-list', request=request),
            'datasets': reverse('v1:dataset-list', request=request),
            'celltypes': reverse('v1:cellline-list', request=request),

            
        })

def api_homepage(request):

    setattr(request, 'view', 'api-home')
    
    setattr(request, 'get_api_host', _get_api_root_url(request))
    setattr(request, 'get_host', _get_host_name(request))

    return render(request, 'rest_framework/api_home.html')

def api_docs(request):

    setattr(request, 'view', 'apidocs')
    setattr(request, 'get_api_host', _get_api_root_url(request))
    setattr(request, 'get_host', _get_host_name(request))

    return render(request, 'rest_framework/api_docs.html')


def api_live(request):

    setattr(request, 'view', 'apilive')
    setattr(request, 'get_api_host', _get_api_root_url(request))
    setattr(request, 'get_host', _get_host_name(request))

    return render(request, 'rest_framework/api_live.html')

def api_contactus(request):

    setattr(request, 'view', 'contactus')
    setattr(request, 'get_api_host', _get_api_root_url(request))
    setattr(request, 'get_host', _get_host_name(request))

    return render(request, 'rest_framework/api_contact.html')

def api_overview(request):

    setattr(request, 'view', 'overview')
    setattr(request, 'get_api_host', _get_api_root_url(request))
    setattr(request, 'get_host', _get_host_name(request))

    return render(request, 'rest_framework/api_overview.html')

def api_clients(request):

    setattr(request, 'view', 'clients')
    setattr(request, 'get_api_host', _get_api_root_url(request))
    setattr(request, 'get_host', _get_host_name(request))

    return render(request, 'rest_framework/api_clients.html')

def _get_api_root_url(request):
    return request.build_absolute_uri(location='/')+'api/v1/'


def _get_host_name(request):
    return request.build_absolute_uri(location='/')


    

