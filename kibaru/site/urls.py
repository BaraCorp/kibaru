#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url
from kibaru.site import views

urlpatterns = patterns('',
                       url(r'^(?P<slug>[-\w\d]*)$',
                           views.home, name='home'),
                       url(r'^display_article/(?P<slug>[-\w\d]*)$',
                           views.display_article, name='display_article'),
                       url(r'^display_new/(?P<id>\d+)$',
                           views.display_new, name='display_new'),
                       url(r'^display_publicity/(?P<id>\d+)$',
                           views.display_publicity, name='display_publicity'),
                       url(r'^article/(\d{4,4})/$', views.year_view, name='article_year'),
                       url(r'^article/(\d{4,4})/(\d{2,2})/$', views.month_view, name='article_month'),
                       # url(r'^article/tag/([\w\-]+)/$', views.tag_view),
                       url(r'^search/$', views.search, name='search'),
                       )
