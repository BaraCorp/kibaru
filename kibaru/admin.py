#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.contrib import admin

from .models import Category, Member, News, Article, Newsletter

admin.site.register(Category)
admin.site.register(Member)
admin.site.register(News)
admin.site.register(Article)
admin.site.register(Newsletter)
