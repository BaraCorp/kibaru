from __future__ import unicode_literals

from django.conf.urls import patterns, url
from kibaru.site import views

urlpatterns = patterns('',
                       url(r'^(?P<slug>[a-zA-Z0-9\-]+)*$',
                           views.home, name='home'),
                       url(r'^display_article/(?P<slug>[-\w\d]+)*$',
                           views.display_article, name='display_article'),
                       url(r'^display_publicity/(?P<id>\d+)$',
                           views.display_publicity, name='display_publicity'),
                       url(r'^article/(\d{4,4})/$', views.year_view),
                       url(r'^article/(\d{4,4})/(\d{2,2})/$',
                           views.month_view),
                       url(r'^article/tag/([\w\-]+)/$', views.tag_view),
                       url(r'^search/$', views.search),
                       )
