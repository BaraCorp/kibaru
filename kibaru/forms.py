#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from kibaru.models import (Article, Directory, Member, New, Newsletter, Video)


class Articleform(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['slug', 'date_created', 'date_modified', 'thumbnail',
                   'count_like', 'count_view', 'author']
        widgets = {
            'legend': forms.TextInput(attrs={
                'placeholder': "Legende de l'image"}),
        }


class Newform(forms.ModelForm):

    class Meta:
        model = New
        exclude = ['count_like', 'count_view', 'author']


class Newsletterform(forms.ModelForm):

    class Meta:
        model = Newsletter
        exclude = ['date']
        widgets = {
            'legend': forms.TextInput(attrs={
                'placeholder': "{{form.email.label}}"}),
        }


class DirectoryFrom(forms.ModelForm):

    class Meta:
        model = Directory
        exclude = ['date_created']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom du site'}),
            'domaine': forms.TextInput(attrs={
                'placeholder': 'Exemple : https://kibaru.ml'}),
            'logo': forms.TextInput(attrs={
                'placeholder': 'Exemple : https://kibaru.ml/static/logo.svg'}),
            'description': forms.Textarea(
                attrs={'placeholder': _('Enter description here')}),
        }


class Videoform(forms.ModelForm):

    class Meta:
        model = Video
        exclude = ['date_created']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'Exp: 6reLVhqXxy8'}),
            'title': forms.TextInput(attrs={'placeholder': 'Info. '}),
        }


class UserCreationForm(forms.ModelForm):

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = (
            'email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
