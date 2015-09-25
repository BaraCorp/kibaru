from __future__ import unicode_literals

from django.conf.urls import patterns, url
from kibaru.site import views


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^display_article/(?P<id>\d+)$', views.display_article, name='display_article'),
                       url(r'^display_publicity/(?P<id>\d+)$', views.display_publicity, name='display_publicity'),
                       )
