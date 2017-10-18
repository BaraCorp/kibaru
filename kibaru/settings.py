#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

from django.utils.translation import gettext_lazy as _

abs_path = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(abs_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3(p&^=gsgxk84xf8s4-rqpob41t7rrwp(tqm_enwxr2ov^!bf='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

LOGGING_CONFIG = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'cities': {
            'handlers': ['console'],
            'level': 'INFO'
        },

    }
}
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'kibaru',
    'tinymce',
    'imagefit',
    'widget_tweaks',
    'disqus',
    'dbbackup',  # django-dbbackup
    'poll',
    'sorl.thumbnail',
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
    'django.middleware.locale.LocaleMiddleware',
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
                "django.core.context_processors.i18n",
            ],
        },
    },
]

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SENDER = 'root@localhost'

AUTH_USER_MODEL = 'kibaru.Member'

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

LANGUAGES = (
    ('fr', _('French')),
    # ('en', _('English')),
    ('ar', _('Arabic')),
)

LANGUAGE_CODE = 'fr-fr'
DEFAULT_LANGUAGE = 1
DATE_INPUT_FORMATS = ('%Y-%m-%d')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(ROOT_DIR, "locale"),
    os.path.join(ROOT_DIR, "kibaru/locale"),
)

MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
STATIC_URL = '/static/'


DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

FACEBOOK_PAGE = "Kibaruu-1652451611660511"
FACEBOOK_USER = "kibaruuml"
FACEBOOK_APP_ID = "1652451611660511"

AR_LEDIT = "ar_ledit.pdf"
FR_LEDIT = "fr_ledit.pdf"

# TWITTER_MAXLENGTH = 140
TWITTER_NAME = "kibml"
APP_NAME = "kibaru"
DOMMAIN = "https://kibaru.ml"
GOOGLE_PLUS = "112702821247370813954"
YOUTUBE = "kibaruuml"
GMAIL = "kibaruuml@gmail.com"
TEL1 = ""
TEL2 = ""
ADDRESS = ""
BP = ""

FIXTURE_DIRS = (
    os.path.join(ROOT_DIR, 'fixtures'),
)

IMAGEFIT_PRESETS = {
    'img_start': {'width': 550, 'height': 450, 'crop': True},
    'img_artd': {'width': 760, 'height': 550, 'crop': True},
    'img_art': {'width': 407, 'height': 200, 'crop': True},
}

try:
    from kibaru.settings_local import *
except Exception as e:
    print(e)
