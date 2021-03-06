#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from django.contrib import admin
# from django.db import models

# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from kibaru.forms import (Articleform, DirectoryFrom,
                          UserChangeForm, UserCreationForm, Videoform)
from kibaru.models import (Article, Category, Directory, Job, Language, Member,
                           New, Newsletter, Publicity, Video)
# from import_export.admin import ImportExportModelAdmin
# unregister and register again
# admin.site.unregister(Group)


@admin.register(Member)
class MemberAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'date_of_birth', 'email',)}),
        ('Permissions', {'fields': ('groups', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide', 'extrapretty'),
                'fields': ('username', 'password1', 'password2', )}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'date_of_birth', 'email')}),
        ('Permissions', {'fields': ('groups', 'is_admin')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'lang', 'date_created', 'twitte', 'date_expired',
                    'count_view', 'author', 'slug')
    list_filter = ('lang', 'date_created', 'date_expired',
                   'author', 'type_notice')

# @admin.register(Choice)
# class CceoixAdmin(admin.ModelAdmin):
#     pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'author', 'date', 'count_view')
    list_filter = ('lang', 'author', 'type_new', 'twitte',)

    exclude = ('slug',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass


@admin.register(Publicity)
class PublicityAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'lang', 'date_created', 'twitte', 'date_modified',
                    'status', 'category', 'count_view', 'author', 'slug')
    list_filter = ('lang', 'date_created', 'status', 'author', 'category')
    fieldsets = (
        ('Article', {'fields': ('image', 'twitte', 'legend', 'title', 'text',
                                'lang', 'date_created', 'category')}),
        ('Auteur', {'fields': ('author',)}),
        (None, {'fields': ('start', 'status')}),
    )
    exclude = ('slug',)
    form = Articleform


# @admin.register(Article)
# class ArticleAdmin(ImportExportModelAdmin):
#     pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = Videoform


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    form = DirectoryFrom
