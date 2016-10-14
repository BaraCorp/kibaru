#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin
from django.db import models

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from kibaru.models import (Language, Category, Member, New, Article,
                           Newsletter, Publicity, Video)
from kibaru.forms import (Articleform, Videoform, UserChangeForm,
                          UserCreationForm)

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_created', 'date_modified', 'status',
                    'category', 'count_view', 'slug')
    list_filter = ('lang', 'date_created', 'status', 'author', 'category')
    fieldsets = (
        ('Article', {
         'fields': ('image', 'title', 'text',  'lang', 'date_created', 'category')}),
        ('Auteur', {'fields': ('author',)}),
        (None, {'fields': ('start', 'status')}),
    )
    exclude = ('slug',)
    form = Articleform


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = Videoform
