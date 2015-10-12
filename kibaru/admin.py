#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin
from django.db import models

from kibaru.models import Category, Member, New, Article, Newsletter, Publicity
from kibaru.form import Articleform


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: {'input_formats': ('%m/%d/%Y',)},
    }


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass


@admin.register(Publicity)
class PublicityAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    form = Articleform
