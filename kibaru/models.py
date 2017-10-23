#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import datetime
import os
import re
# from django.core.urlresolvers import reverse

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core import validators

from django.db import models
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

from django_resized import ResizedImageField

from kibaru.tools import social_share

from py3compat import implements_to_string

import short_url

from tinymce import models as tinymce_models


@implements_to_string
class Directory(models.Model):

    """ Annuaire des sites du Mali"""
    class Meta:
        verbose_name = _('Directory')
        verbose_name_plural = _('Directories')

    INFO = "I"
    MUSIC = "M"
    SPORT = "C"

    TYPE_SITE_CHOICES = {
        INFO: _('info'),
        MUSIC: _('Music'),
        SPORT: _('Sport'),
    }

    name = models.CharField(
        verbose_name=_("Name"), max_length=75, primary_key=True)
    category = models.CharField(verbose_name=_("Category"), max_length=50,
                                choices=TYPE_SITE_CHOICES.items(),
                                default=INFO)
    domaine = models.CharField(
        verbose_name=_("adress of site"), max_length=150)
    logo = models.CharField(verbose_name=_("Logo"), max_length=150)
    description = models.TextField(
        _("Description"), max_length=150, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Dated the"),
                                        default=timezone.now)

    def __str__(self):
        return "{name}/{date_created}".format(name=self.name,
                                              date_created=self.date_created)


@implements_to_string
class Category(models.Model):

    """ """
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    slug = models.SlugField(_("Slug"), max_length=75, primary_key=True)
    name = models.CharField(_("Name"), max_length=150)

    def __str__(self):
        return "{name}/{slug}".format(name=self.name, slug=self.slug)


class MemberManager(BaseUserManager):

    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=MemberManager.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(username,
                             password=password,
                             date_of_birth=date_of_birth
                             )
        u.is_admin = True
        u.save(using=self._db)
        return u


@implements_to_string
class Language(models.Model):

    FR = "fr"
    EN = "en"
    AR = "ar"
    LANGUAGES_CHOICES = {
        FR: _('French'),
        # EN: _('English'),
        AR: _('Arabic'),
    }

    slug = models.SlugField(max_length=50, verbose_name=_("Slug"),
                            choices=LANGUAGES_CHOICES.items())
    name = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_("Name"))

    def __str__(self):
        return u"({slug}) {name}".format(name=self.name, slug=self.slug)


@implements_to_string
class Member(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    username = models.CharField(
        _("username"), max_length=50, primary_key=True,
        help_text=_("Required. 50 characters or fewer. "
                    "Letters, numbers and @/./+/-/_ characters"),
        validators=[
            validators.RegexValidator(re.compile("^[\w.@+-]+$"),
                                      _("Enter a valid username."),
                                      "invalid")])

    first_name = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, blank=True, null=True,
                                 verbose_name=_("Last Name"))
    image = models.ImageField(upload_to='images_member/', blank=True,
                              verbose_name=_("Photo"))
    job_title = models.CharField(max_length=200, blank=True,
                                 verbose_name=_("Job title"))
    email = models.EmailField(_("email address"), blank=True, null=True)
    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_(
        "Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(
        _("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    date_of_birth = models.DateField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    objects = MemberManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@implements_to_string
class New(models.Model):

    class Meta:
        ordering = ('-date',)
        verbose_name = _('New')
        verbose_name_plural = _('News')

    INFO = "I"
    URGENT = "U"
    COMMUNICATED = "C"

    TYPE_NEWS_CHOICES = {
        INFO: _('info'),
        URGENT: _('urgent'),
        COMMUNICATED: _('communicated'),
    }

    type_new = models.CharField(
        max_length=2, choices=TYPE_NEWS_CHOICES.items(), default=INFO)
    lang = models.ForeignKey(
        Language, blank=True, null=True, verbose_name=_("Language"))
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    comment = models.TextField(blank=True, verbose_name=_("Texte"))
    author = models.ForeignKey(Member, verbose_name=_("Author"))
    date = models.DateTimeField(verbose_name=_("Dated the"),
                                default=datetime.datetime.today)
    count_view = models.IntegerField(default=0, blank=True, null=True)
    count_like = models.IntegerField(default=0, blank=True, null=True)
    twitte = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return "{title} {date}".format(title=self.title, date=self.date)

    @property
    def get_short_id(self):
        # return short_url.encode_url(self.id)
        return "{}".format(self.id)

    @property
    def image(self):
        return None

    def type_text(self):
        return self.TYPE_NEWS_CHOICES.get(self.type_new)

    def is_twitte(self):
        if not self.twitte:
            return False
        self.twitte = False
        return True

    def save(self, *args, **kwargs):
        self.twitter = self.is_twitte()
        super(New, self).save(*args, **kwargs)

    def post_url(self):
        return os.path.join(
            settings.DOMMAIN, self.lang.slug, "new", self.get_short_id)

    def get_twiter_message(self):
        return u"{} - {}".format(self.type_text(), self.title), self.post_url()

models.signals.post_save.connect(social_share, sender=New)


@implements_to_string
class Newsletter(models.Model):

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    lang = models.ForeignKey(
        Language, blank=True, null=True, verbose_name=_("Language"))
    date = models.DateTimeField(verbose_name=_("Registration date"),
                                default=datetime.datetime.today)
    email = models.EmailField(
        max_length=75, verbose_name=_("E-mail"), unique=True)

    def __str__(self):
        return "{email} {date}".format(email=self.email,
                                       date=self.date)


@implements_to_string
class Article(models.Model):

    class Meta:
        ordering = ('-date_created', '-id')
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    DRAFT = 'draft'
    POSTED = 'posted'

    STATUS = {
        DRAFT: _("Draft"),
        POSTED: _("Posted"),
    }
    slug = models.CharField(
        max_length=200, unique=True, blank=True, verbose_name=_("Slug"))
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    text = tinymce_models.HTMLField(blank=True, verbose_name=_("Text"))
    image = ResizedImageField(size=[1024, 500], upload_to='images_article/',
                              blank=True, verbose_name=_("Picture"))
    legend = models.CharField(
        max_length=200, verbose_name=_("legend"), blank=True)
    author = models.ForeignKey(Member, verbose_name=_("Author"))
    date_created = models.DateTimeField(verbose_name=_("Dated the"),
                                        default=datetime.datetime.today)
    date_modified = models.DateTimeField(auto_now=True)
    lang = models.ForeignKey(
        Language, blank=True, null=True, verbose_name=_("Language"))
    category = models.ForeignKey(Category, verbose_name=_("Category"))
    status = models.CharField(verbose_name=_("Status"), max_length=50,
                              choices=STATUS.items())
    start = models.BooleanField(verbose_name=_("Start"), default=False)
    count_view = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    twitte = models.BooleanField(default=True, blank=True)

    @property
    def get_short_id(self):
        return short_url.encode_url(self.id)

    def get_tag_list(self):
        return re.split(" ", self.tags)

    def get_path_img(self):
        return os.path.join("images_article", "{}.jpg".format(
            os.path.splitext(os.path.basename(self.image.name))[0]))

    def convert_to_jpg(self):
        from PIL import Image
        im = Image.open(self.image)
        if not im.format == "JPEG":
            im_path = self.get_path_img()
            im.convert('RGB').save(os.path.join(
                settings.MEDIA_ROOT, im_path), "JPEG", quality=95)
            self.image = im_path

    def save(self, *args, **kwargs):
        self.slug = re.sub(
            "[\!\*\’\(\)\;\:\@\&\=\+\$\,\/\?\#\[\](\-)\s \. \؟]+", '-',
            self.title.lower())
        self.twitter = self.is_twitte()
        if self.image:
            self.convert_to_jpg()

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return "{title} {status}".format(title=self.title, status=self.status)

    def __unicode__(self):
        return "{title} {status}".format(title=self.title, status=self.status)

    def is_twitte(self):
        if self.status == self.DRAFT:
            return False
        if not self.twitte:
            return False
        self.twitte = False
        return True

    def title_status(self):
        return self.STATUS.get(self.status)

    def type_text(self):
        return "{}".format(self.category.name)

    def clean_tags_html(self, linit=150):
        return u"%s" % re.sub(re.compile('<[^<]+?>'), '', self.text)[:linit]

    def post_url(self):
        return os.path.join(
            settings.DOMMAIN, self.lang.slug, "art", self.get_short_id)

    def get_twiter_message(self):
        return u"{} - {}".format(self.type_text(), self.title), self.post_url()

models.signals.post_save.connect(social_share, sender=Article)


@implements_to_string
class Publicity(models.Model):

    class Meta:
        verbose_name = _('Publicity')
        verbose_name_plural = _('Publicities')

    image = models.ImageField(upload_to='images_pub/', blank=True,
                              verbose_name=_("Picture"))

    def __str__(self):
        return self.image


class Video(models.Model):

    class Meta:
        ordering = ('-date_created',)
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    slug = models.CharField(
        max_length=200, unique=True, blank=True, verbose_name=_("Slug"))
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    date_created = models.DateTimeField(verbose_name=_("Date created"),
                                        default=datetime.datetime.today)

    def __str__(self):
        return "{title} {slug}".format(slug=self.slug,
                                       title=self.title)

    def __unicode__(self):
        return "{title} {slug}".format(slug=self.slug,
                                       title=self.title)

    def link(self):
        return "//www.youtube.com/embed/{slug}".format(slug=self.slug)


class Job(models.Model):

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

    N = 'n'
    C = 'c'
    TYPE_NOTICE = {
        N: _("Notice"),
        C: _("Call for tenders")
    }
    type_notice = models.CharField(verbose_name=_("Type"), max_length=50,
                                   choices=TYPE_NOTICE.items(), default=N)
    text = tinymce_models.HTMLField(blank=True, verbose_name=_("Text"))
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    count_view = models.IntegerField(default=0)
    twitte = models.BooleanField(default=True, blank=True)
    author = models.ForeignKey(Member, verbose_name=_("Author"))
    slug = models.CharField(max_length=200,
                            unique=True, blank=True, verbose_name=_("Slug"))
    date_created = models.DateTimeField(
        verbose_name=_("Dated the"), auto_now=True)
    date_expired = models.DateTimeField(
        verbose_name=_("Date expired"), default=datetime.datetime.today)
    lang = models.ForeignKey(Language, blank=True, null=True,
                             verbose_name=_("Language"))

    @property
    def image(self):
        return None

    def job_active(self):
        return Job.objects.filter(date_expired__gte=datetime.datetime.today)

    def __unicode__(self):
        return "{} / {}".format(self.title, self.date_expired)

    def __str__(self):
        return "{} / {}".format(self.title, self.date_expired)

    def is_twitte(self):
        if not self.twitte:
            return False
        self.twitte = False
        return True

    @property
    def get_short_id(self):
        # return short_url.encode_url(self.id)
        return "{}".format(self.id)

    def save(self, *args, **kwargs):
        self.slug = re.sub(
            "[\!\*\’\(\)\;\:\@\&\=\+\$\,\/\?\#\[\](\-)\s \. \؟]+", '-',
            self.title.lower())
        self.twitter = self.is_twitte()
        super(Job, self).save(*args, **kwargs)

    def type_text(self):
        return self.TYPE_NOTICE.get(self.type_notice)

    def post_url(self):
        return os.path.join(
            settings.DOMMAIN, self.lang.slug, "job", self.get_short_id)

    def get_twiter_message(self):
        return u"{} - {}".format(self.type_text(), self.title), self.post_url()

models.signals.post_save.connect(social_share, sender=Job)
