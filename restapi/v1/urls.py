# -*- coding: utf-8 -*-
## Author: Aziz Khan
## License: GPL v3
## Copyright © 2017 Aziz Khan <azez.khan__AT__gmail.com>

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.cache import cache_page

from . import views

#cache timeout in seconds

CACHE_TIMEOUT = 60 * 60 * 24 * 1 # cache timeout in seconds
#CACHE_TIMEOUT = 0


urlpatterns = [
	#url(r'^$', cache_page(CACHE_TIMEOUT)(views.APIRoot.as_view()), name='api-root'),	

    url(r'^v1/$', views.APIRoot.as_view(), name='api-root'),

    url(r'^v1/tfs/?$', cache_page(CACHE_TIMEOUT)(views.TranscriptionFactorListViewSet.as_view()), name='tf-list'),
    url(r'^v1/tfs/(?P<tf_id>.+)/$', cache_page(CACHE_TIMEOUT)(views.TranscriptionFactorDetailsViewSet.as_view()), name='tf-detail'),
    #url(r'^v1/tfs/(?P<tf_name>\w+)/(?P<tf_id>\w+)/$', cache_page(CACHE_TIMEOUT)(views.TranscriptionFactorDetailsViewSet.as_view()), name='tf-list'),


    url(r'^v1/datasets/?$', cache_page(CACHE_TIMEOUT)(views.DatasetListViewSet.as_view()), name='dataset-list'),    

    url(r'^v1/celltypes/?$', cache_page(CACHE_TIMEOUT)(views.CelllineListViewSet.as_view()), name='cellline-list'),
    url(r'^v1/celltypes/(?P<cell_line>\w+)/$', cache_page(CACHE_TIMEOUT)(views.CelllineFactorListViewSet.as_view()), name='cellline-detail'),
    # #url(r'^v1/species/(?P<tax_id>\w+)/matrix$', views.SpeciesMatrixListViewSet.as_view(), name='specie-detail'),
    
    # url(r'^v1/infer/(?P<sequence>\w+)/$', cache_page(CACHE_TIMEOUT)(views.MatrixInferenceViewSet.as_view()), name='matrix-infer'),
    
    # url(r'^v1/tffm/?$', cache_page(CACHE_TIMEOUT)(views.TFFMListViewSet.as_view()), name='tffm-list'),
    # url(r'^v1/tffm/(?P<tffm_id>.+)/$', cache_page(CACHE_TIMEOUT)(views.TFFMDetailsViewSet.as_view()), name='tffm-detail'),

    # url(r'^v1/releases/?$', cache_page(CACHE_TIMEOUT)(views.ReleaseListViewSet.as_view()), name='release-list'),
    # url(r'^v1/releases/(?P<release_number>.+)/$', cache_page(CACHE_TIMEOUT)(views.ReleaseDetailsViewSet.as_view()), name='release-detail'),

    #url(r'^v1/docs', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION), name='api-docs'),

    url(r'^home/?$', views.api_homepage, name='api-homepage'),
    url(r'^v1/?$', views.api_homepage, name='api-homepage'),
    #url(r'^docs/?$', views.api_docs, name='api-docs'),
    url(r'^v1/live-api/?$', views.api_live, name='api-live'),
    url(r'^contact-us/?$', views.api_contactus, name='api-contactus'),
    url(r'^overview/?$', views.api_overview, name='api-overview'),
    url(r'^clients/?$', views.api_clients, name='api-clients'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json','jsonp','bed','yaml','api'])
