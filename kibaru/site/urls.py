#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url

from kibaru.site import views

urlpatterns = patterns('',
                       url(r'^(?P<slug>[-\w\d]*)$', views.home, name='home'),
                       url(r'^directory/$', views.directory, name='directory'),
                       url(r'^art/(?P<slug>.*)',
                           views.display_article, name='art'),
                       url(r'^new/(?P<id>[-\w\d]*)$',
                           views.display_new, name='news'),
                       url(r'^display_publicity/(?P<id>\d+)$',
                           views.display_publicity, name='display_publicity'),
                       url(r'^article/(\d{4,4})/$',
                           views.year_view, name='article_year'),
                       url(r'^article/(\d{4,4})/([-\w\d]*)/$',
                           views.month_view, name='article_month'),
                       # url(r'^article/tag/([\w\-]+)/$', views.tag_view),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^videos/$', views.display_videos,
                           name='all_videos'),
                       url(r'^sport/$', views.display_heading,
                           name='all_sport'),
                       url(r'^art/$', views.display_heading,
                           name='all_sport'),
                       url(r'^culture/$', views.display_heading,
                           name='all_sport'),
                       )
