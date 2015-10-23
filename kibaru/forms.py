#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django import forms
from kibaru.models import Article, New


class Articleform(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['slug', 'date_created', 'date_modified', 'thumbnail',
                   'count_like', 'count_view']


class Newform(forms.ModelForm):

    class Meta:
        model = New
        exclude = []
