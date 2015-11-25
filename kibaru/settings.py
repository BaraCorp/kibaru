#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import os

abs_path = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(abs_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3(p&^=gsgxk84xf8s4-rqpob41t7rrwp(tqm_enwxr2ov^!bf='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kibaru',
    'tinymce',
    'widget_tweaks',
    'disqus',
    'django.contrib.sites',
    "social_widgets",
    'imagefit',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'kibaru.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kibaru.wsgi.application'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGES = (('fr', "French"),)
LANGUAGE_CODE = 'fr-fr'

DATE_INPUT_FORMATS = ('%Y-%m-%d')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
STATIC_URL = '/static/'

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

FACEBOOK_PAGE = "https://www.facebook.com/BaraCorp-1557724531167282"
FACEBOOK_USER = "kibaruuml"
FACEBOOK_APP_ID = "1651809315058736"

TWITTER_USER = "kibml"
APP_NAME = "kibaruu"

GOOGLE_PLUS = "112702821247370813954"
YOUTUBE = "kibaruuml"
GMAIL = "kibaruuml@gmail.com"
TEL1 = ""
TEL2 = ""
ADDRESS = ""
BP = ""


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

try:
    from kibaru.settings_local import *
except Exception as e:
    print(e)
