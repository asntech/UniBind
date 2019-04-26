## Author: Aziz Khan
## License: GPL v3
## Copyright 2017 Aziz Khan <azez.khan__AT__gmail.com>


"""jaspar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
API_TITLE = 'UniBind API'
API_DESCRIPTION = 'This API provides easy-to-use REST web interface to query/retrieve matrix profile data from the latest version of UniBind database. \
The API comes with a human browsable interface and also programmatic interface, which return the results in eight different formats, including <code>json</code>, <code>jsonp</code>, <code>jaspar</code>, <code>meme</code>, <code>transfac</code>, <code>pfm</code>, <code>yaml</code> and <code>bed</code>'


from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from rest_framework.documentation import include_docs_urls, get_docs_view

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

from restapi.v1.views import APIRoot

sitemaps = {
    'static': StaticViewSitemap,
}

admin.site.site_header = 'UniBind Admin'

from rest_framework_swagger.views import get_swagger_view
swagger_schema_view = get_swagger_view(title='UniBind Live API')

from rest_framework.schemas import get_schema_view
schema_view = get_schema_view(
    title='UniBind REST API',
    #url='/api/v1'
)

docs_view = get_docs_view(title=API_TITLE,
    description=API_DESCRIPTION
    )

urlpatterns = [
    url(r'^', include('portal.urls')),

    url(r'^admin/', admin.site.urls),
    
    url(r'^api/', include('restapi.v1.urls', namespace='v1')),

    url(r'^api/v1/docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    url(r'^api/v1/docs', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, schema_url='')),

    url(r'^api/v1/', schema_view),

    url(r'^api/v1/docs/', include('restapi.v1.urls', namespace='api-docs')), 

    url(r'^api/v1/live/', swagger_schema_view),

    url(r'^api/v1/$', APIRoot.as_view(), name='api-root'),
      
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


