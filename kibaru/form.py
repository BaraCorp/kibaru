#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from kibaru.models import Article


class Articleform(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['slug', 'date_created', 'date_modified']
