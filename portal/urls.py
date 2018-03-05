## Author: Aziz Khan
## License: GPL v3
## Copyright 2017 Aziz Khan <azez.khan__AT__gmail.com>

from django.conf.urls import url
from django.conf.urls import handler404, handler500
from . import views
from unibind import settings
from django.views.static import serve


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/?$', views.search, name='search'),
    url(r'^docs/$', views.documentation, name='documentation'),
    url(r'^contact-us/?$', views.contact_us, name='contact_us'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^changelog/$', views.changelog, name='changelog'),
    
    #API documentation
    url(r'^api/$', views.api_documentation, name='api_documentation'),
    
    url(r'^factor/(?P<factor_id>[\w.]+)/$', views.factor_detail, name='factor_detail'),

    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)$', views.post_details, name='post_details'),
    url(r'^blog/$', views.post_list, name='post_list'),

    url(r'^tour/$', views.tour_video, name='tour_video'),

    url(r'^downloads/$', views.download_data, name='download_data'),

    #enable this url to create zip/txt files for downloads page
    #url(r'^downloads-internal/$', views.internal_download_data, name='internal_download_data'),
    
    url(r'^temp/(?P<path>.*)$', serve, {'document_root': settings.TEMP_DIR}),
    url(r'^download/(?P<path>.*)$', serve, {'document_root': settings.DOWNLOAD_DIR, 'show_indexes': True,}),

]

handler404 = 'portal.views.page_not_found'
handler500 = 'portal.views.server_error'


