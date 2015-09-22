from __future__ import unicode_literals

from django.conf.urls import patterns, url
from kibaru.site import views


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home')
                       )
