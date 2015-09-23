#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.contrib import admin

from .models import Category, Member, New, Article, Newsletter, Publicity

admin.site.register(Category)
admin.site.register(Member)
admin.site.register(New)
admin.site.register(Article)
admin.site.register(Newsletter)
admin.site.register(Publicity)
