#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
from django_resized import ResizedImageField


import datetime
import re

from django.core import validators
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        UserManager)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from py3compat import implements_to_string


@implements_to_string
class Category(models.Model):

    """ """
    slug = models.SlugField("Code", max_length=75, primary_key=True)
    name = models.CharField(u"Nom", max_length=150)

    def __str__(self):
        return "{name}/{slug}".format(name=self.name, slug=self.slug)


@implements_to_string
class Member(AbstractBaseUser):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(
        _("username"), max_length=50, primary_key=True,
        help_text=_("Required. 50 characters or fewer. "
                    "Letters, numbers and @/./+/-/_ characters"),
        validators=[validators.RegexValidator(re.compile("^[\w.@+-]+$"),
                                              _("Enter a valid username."), "invalid")])

    first_name = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, blank=True, null=True,
                                 verbose_name=_("Last Name"))
    image = models.ImageField(upload_to='images_member/', blank=True,
                              verbose_name=("Photo"))
    job_title = models.CharField(max_length=200, blank=True,
                                 verbose_name=("Poste"))
    email = models.EmailField(_("email address"), blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"), default=False,
        help_text=_("Designates whether the user can "
                    "log into this admin site."))
    is_active = models.BooleanField(
        _("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    def __str__(self):
        return self.name()

    def get_short_name(self):
        return self.name()

    def name(self):
        if not self.first_name and not self.last_name:
            return self.username
        elif not self.first_name:
            return self.last_name
        else:
            return self.first_name


@implements_to_string
class New(models.Model):

    """ """
    title = models.CharField(max_length=100, verbose_name=("Titre"))
    comment = models.TextField(blank=True, verbose_name=("Contenu"))
    author = models.ForeignKey(Member, verbose_name=("Auteur"))
    date = models.DateField(verbose_name=("Fait le"),
                            default=datetime.datetime.today)

    def __str__(self):
        return "{title} {date}".format(title=self.title, date=self.date)


@implements_to_string
class Newsletter(models.Model):

    """ """
    date = models.DateField(verbose_name=("Date d'inscription"),
                            default=datetime.datetime.today)
    email = models.EmailField(
        max_length=75, verbose_name=("E-mail"), unique=True)

    def __str__(self):
        return "{email} {date}".format(email=self.email,
                                       date=self.date)


@implements_to_string
class Article(models.Model):
    DRAFT = 'draft'
    POSTED = 'posted'

    STATUS = {
        DRAFT: "Brouillon",
        POSTED: "Publié",
    }
    slug = models.CharField(
        max_length=200, unique=True, blank=True, verbose_name=("Slug"))
    title = models.CharField(max_length=200, verbose_name=("Titre"))
    text = models.TextField(blank=True, verbose_name=("Texte"))
    image = ResizedImageField(
        size=[1024, 578], upload_to='images_article/', blank=True,
        verbose_name=("Image"))
    thumbnail = ResizedImageField(
        size=[187, 103], upload_to='images_article', blank=True)
    author = models.ForeignKey(Member, verbose_name=("Auteur"))
    date_created = models.DateField(verbose_name=("Fait le"),
                                    default=datetime.datetime.today)
    date_modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, verbose_name=("Categorie"))
    status = models.CharField(verbose_name="Status", max_length=50,
                              choices=STATUS.items())
    start = models.BooleanField(verbose_name="Start", default=False)

    def get_tag_list(self):
        return re.split(" ", self.tags)

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(" ", "-").lower()
        self.thumbnail = self.image
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return "{title} {status}".format(title=self.title, status=self.status)

    def title_status(self):
        return self.STATUS.get(self.status)


@implements_to_string
class Publicity(models.Model):
    image = models.ImageField(upload_to='images_pub/', blank=True,
                              verbose_name=("Photo"))

    def __str__(self):
        return self.image.__str__()
