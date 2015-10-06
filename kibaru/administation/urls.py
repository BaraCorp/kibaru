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
                       url(r'^edit_article/(?P<id>\d+)$', views.edit_article, name='edit_article'),
                       url(r'^del_article/(?P<id>\d+)$', views.del_article, name="del_article"),
                       )
