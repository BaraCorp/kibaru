#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.contrib import admin

from .models import Category, Member, New, Article, Newsletter, Publicity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    pass


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass


@admin.register(Publicity)
class PublicityAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # fields = ('date_created', 'title', 'category',
    #           'status', 'tags', 'text', 'image')
    exclude = ('slug',)
