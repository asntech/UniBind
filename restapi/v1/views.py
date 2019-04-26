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
    max_page_size = 1000


def _get_sequence_logo(request, base_id, version):
    host_name = request.build_absolute_uri(location='/')
    return  str(host_name)+'static/logos/svg/'+base_id+'.'+str(version)+'.svg'

def _get_matrix_url(request, base_id, version):

    host_name = request.build_absolute_uri(location='/')
    return  str(host_name)+'api/v1/matrix/'+base_id+'.'+str(version)

def _get_sites_fasta_url(request, base_id, version):

    if os.path.isfile(BASE_DIR+'/download/sites/'+base_id+'.'+str(version)+'.sites'):
        host_name = request.build_absolute_uri(location='/')
        return  str(host_name)+'download/sites/'+base_id+'.'+str(version)+'.sites'
    else:
        return None

def _get_sites_bed_url(request, base_id, version):

    if os.path.isfile(BASE_DIR+'/download/bed_files/'+base_id+'.'+str(version)+'.bed'):
        host_name = request.build_absolute_uri(location='/')
        return  str(host_name)+'download/bed_files/'+base_id+'.'+str(version)+'.bed'
    else:
        return None

def _get_peaks_url(request, factor_id):
    return  str(request.build_absolute_uri(location='/'))+'static/data/peaks/macs/'+factor_id+'/'+factor_id+'.narrowPeak'


def _get_tffm_url(request, base_id, version, trained_order):

    if os.path.isfile(BASE_DIR+'/static/TFFM/'+base_id+'.'+str(version)+'/TFFM_'+trained_order+'_trained.xml'):
        host_name = request.build_absolute_uri(location='/')
        return  str(host_name)+'static/TFFM/'+base_id+'.'+str(version)+'/TFFM_'+trained_order+'_trained'
    else:
        return None


def _get_cellline_url(request, cell_line):
    host_name = request.build_absolute_uri(location='/')
    return  str(host_name)+'api/v1/celltypes/'+cell_line+'/'

def _get_tf_url(request, tf_name):
    host_name = request.build_absolute_uri(location='/')
    return  str(host_name)+'api/v1/tfs/'+tf_name+'/'

def _get_taxon_url(request, tax_group):
    host_name = request.build_absolute_uri(location='/')
    return  str(host_name)+'api/v1/taxon/'+tax_group+'/'



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
    API endpoint that returns the matrix profile detail information.
    """
    #queryset = Matrix.objects.all()

    parser_classes = (YAMLParser,)
    renderer_classes = [renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    #@view_config(response_serializer=MatrixSerializer)
    def get(self, request, tf_id, format=None):
        """
        Gets profile detail information
        """

        setattr(request, 'view', 'api-browsable')

        #split base_id and version
        
        data_dict = {}


        factor = Factor.objects.get(folder=tf_id)
        #factor = Factor.objects.values().get(folder=factor_id)

        factordata = FactorData.objects.values().filter(folder=tf_id)
        #factordata = FactorData.objects.filter(folder=tf_id)

        data_dict = {
                
                'tf_name': factor.tf_name,
                "cell_line": factor.cell_line,
                "biological_condition": factor.biological_condition,
                "identifier": factor.identifier,
                'jaspar_id': factor.jaspar_id+'.'+str(factor.jaspar_version),
                "tf_id": factor.folder,
                "total_peaks": factor.total_peaks,
                #'sequence_logo': _get_sequence_logo(request, base_id, version),
                #'versions_url': _get_versions_url(request, base_id),
                'peaks_url': _get_peaks_url(request, tf_id),
            }
        
        prediction_models = ['PWM','DNAshaped','TFFM','DiMo']

        #factordata.values('prediction_model').distinct()

        data_dict.update({'prediction_models': prediction_models})
        #data_dict.update(factor)

        data_dict.update({'tfbs': factordata})

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
                description= 'Taxonomic group. For example: Vertebrates',
                title= 'Cell line',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='biological_condition',
            location='query',
            schema=coreschema.String(
                description= 'Taxa ID. For example: 9606 for Human & 10090 for Mus musculus. Multiple IDs can be added separated by commas (e.g. tax_id=9606,10090).',
                title= 'biological condition',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='identifier',
            location='query',
            schema=coreschema.String(
                description= 'Transcription factor class. For example: Zipper-Type',
                title= 'Identifier',
                ),
            required=False,
            type='string'),
        coreapi.Field(
            name='jaspar_id',
            location='query',
            schema=coreschema.String(
                description= 'If set to latest, return latest version',
                title= 'jaspar id',
                ),
            required=False,
            type='string')
        ]

    def filter_queryset(self, request, queryset, view):

        query_string = request.GET.get('search', None)
        collection = request.GET.get('collection', None)
        tax_group = request.GET.get('tax_group', None)
        tax_id = request.GET.get('tax_id', None)
        tf_class = request.GET.get('tf_class', None)
        tf_family = request.GET.get('tf_family', None)
        data_type = request.GET.get('data_type', None)
        version = request.GET.get('version', None)
        name = request.GET.get('name', None)

        #if collection is set then filter queryset
        if collection and collection !='':
            queryset = queryset.filter(collection=collection.upper())

        #if name is set then filter queryset
        if name and name !='':
            queryset = queryset.filter(name=name)

        #if tax_group is set then filter queryset
        if tax_group and tax_group !='':
            matrix_ids = MatrixAnnotation.objects.values_list('matrix_id', flat=True).filter(tag='tax_group',val=tax_group.lower())
            queryset = queryset.filter(id__in=matrix_ids)

        #if tax id is set then filter queryset
        if tax_id and tax_id !='':
            tax_ids = tax_id.split(',')
            queryset = queryset.filter(id__in = MatrixSpecies.objects.values_list('matrix_id', flat=True).filter(tax_id__in=tax_ids))
     
        #if tf_class is set then filter queryset
        if tf_class and tf_class !='':
            matrix_ids = MatrixAnnotation.objects.values_list('matrix_id', flat=True).filter(tag='class', val__icontains=tf_class)
            queryset = queryset.filter(id__in=matrix_ids)

        #if tf_family is set then filter queryset
        if tf_family and tf_family !='':
            matrix_ids = MatrixAnnotation.objects.values_list('matrix_id', flat=True).filter(tag='family', val__icontains=tf_family)
            queryset = queryset.filter(id__in=matrix_ids)

        #if data_type is set then filter queryset
        if data_type and data_type !='':
            matrix_ids = MatrixAnnotation.objects.values_list('matrix_id', flat=True).filter(tag='type', val__icontains=data_type)
            queryset = queryset.filter(id__in=matrix_ids)

        #if query string is set then filter queryset
        if query_string and query_string != '':
            queryset = queryset.filter(
            Q(name__icontains=query_string) | 
            Q(base_id__icontains=query_string) |
            Q(collection__icontains=query_string)).distinct()

        #if version is latest
        if version in ['latest', 'current']:
            #latest_versions = queryset.values('base_id').annotate(Max('version'))
            #queryset = queryset.filter(version=latest_versions.values('version__max'))#.order_by('version')
            Q_statement = Q()
            latest_versions = queryset.values('base_id').annotate(latest_version=Max('version')).order_by()
            for version in latest_versions:
                Q_statement |=(Q(base_id__exact=version['base_id']) & Q(version=version['latest_version']))

            queryset = queryset.filter(Q_statement)

        return queryset.order_by('name')

class TranscriptionFactorListViewSet(ListAPIView):
    """
    API endpoint that returns a list of all transcription factors.
    """

    filter_backends = [SearchFilter, OrderingFilter,]
    search_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    filter_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    parser_classes = (YAMLParser,)
    renderer_classes = [renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    def get(self, request, format=None):
      """
      List all the collections are available in JASPAR.
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


class DatasetListViewSet(ListAPIView):
    """
    REST API endpoint that returns a list of all the datasets used.
    """
    
    serializer_class = FactorSerializer
    pagination_class = FactorResultsSetPagination
    throttle_classes = (UserRateThrottle,)
    filter_backends = [SearchFilter, OrderingFilter, ]
    search_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    filter_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    parser_classes = (YAMLParser,)
    renderer_classes = [ renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    def get_queryset(self):
        """
        List all Datasets
        """

        setattr(self.request, 'view', 'api-browsable')
        queryset = Factor.objects.all().order_by('tf_name')

        return queryset


class CelllineListViewSet(ListAPIView):
    """
    API endpoint that returns a list of all collection names.
    """

    filter_backends = [SearchFilter, OrderingFilter,]
    search_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    filter_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    parser_classes = (YAMLParser,)
    renderer_classes = [renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    def get(self, request, format=None):
      """
      List all the collections are available in JASPAR.
      """
      setattr(self.request, 'view', 'api-browsable')

      queryset = Factor.objects.values_list('cell_line', flat=True).distinct()
      
      data_dict = { 'count': queryset.count() }
      results = []
      for cell_line in queryset:
        results.append({
        'cell_line': cell_line,
        'url': _get_cellline_url(request, cell_line)
        })

      data_dict.update({'results': results})

      return Response(data_dict)

class CelllineFactorListViewSet(ListAPIView):
    """
    REST API endpoint that returns a list of all the transcription factors.
    """
    
    serializer_class = FactorSerializer
    pagination_class = FactorResultsSetPagination
    throttle_classes = (UserRateThrottle,)
    filter_backends = [SearchFilter, OrderingFilter, ]
    search_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    filter_fileds = ['folder','tf_name', 'cell_line','biological_condition','data_source','jaspar_id']
    parser_classes = (YAMLParser,)
    renderer_classes = [ renderers.JSONRenderer, JSONPRenderer, YAMLRenderer, renderers.BrowsableAPIRenderer]

    def get_queryset(self):
        """
        List all Datasets
        """

        setattr(self.request, 'view', 'api-browsable')

        queryset = Factor.objects.all().order_by('tf_name')

        cell_line = self.kwargs['cell_line']

        #if tax group is set then filter queryset
        if cell_line and cell_line !='':
            
            queryset = queryset.filter(cell_line=cell_line).order_by('name')
        else:
            queryset = None

        return queryset



class APIRoot(APIView):
    """
    This is the root of the UniBind RESTful API v1. Please read the documentation for more details.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=format):
        setattr(request, 'view', 'api-browsable')
        return Response({
            'tf': reverse('v1:tf-list', request=request),
            #'tffm': reverse('v1:tffm-list', request=request),
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


    

