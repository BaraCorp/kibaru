#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url
from kibaru.administation import views


urlpatterns = patterns('',
                       url(r'^$', views.home, name='admin_home'),
                       url(r'^add_article/$', views.add_article, name='add_article'),
                       url(r'^add_new/$', views.add_new, name='add_new'),
                       url(r'^add_video/$', views.add_video, name='add_video'),
                       url(r'^edit_article/(?P<id>\d+)$', views.edit_article, name='edit_article'),
                       url(r'^del_article/(?P<id>\d+)$', views.del_article, name="del_article"),
                       url(r'^del_video/(?P<id>\d+)$', views.del_video, name="del_video"),
                       url(r'^edit_new/(?P<id>\d+)$', views.edit_new, name='edit_new'),
                       url(r'^del_new/(?P<id>\d+)$', views.del_new, name="del_new"),
                       )
