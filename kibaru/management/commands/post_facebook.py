#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os

import facebook
import urllib
import urlparse
import subprocess
import warnings
import requests

from django.conf import settings
from django.core.management.base import BaseCommand
from kibaru.models import Article

# Hide deprecation warnings. The facebook module isn't that up-to-date
# (facebook.GraphAPIError).
warnings.filterwarnings('ignore', category=DeprecationWarning)


# Parameters of your app and the id of the profile you want to mess with.


class Command(BaseCommand):
    help = 'Closes the specified apptts for voting'

    def add_arguments(self, parser):
        # parser.add_argument('apptts_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        print("handle")

        art = Article.objects.all()[0]
        data = {'status': art.text}
        media = {}
        image = art.image
        if image:
            url_img = os.path.join(settings.MEDIA_ROOT, image.name)
            file = open(url_img, 'rb')
            media.update({'media[]': file.read()})
        # print(data)
        token = self.get_fb_token(
            settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
        print(token)

        auth_token = facebook.GraphAPI.get_app_access_token(settings.FACEBOOK_APP_ID,
                                                            settings.FACEBOOK_APP_SECRET)
        print(auth_token)
        graph = facebook.GraphAPI(auth_token)
        graph.put_object(
            "1652451611660511", "feed", message='My message goes here')
        # self.post_facebook(token)

    def get_fb_token(self, app_id, app_secret):
        payload = {'grant_type': 'client_credentials',
                   'client_id': app_id, 'client_secret': app_secret}
        file = requests.post(
            'https://graph.facebook.com/oauth/access_token?', params=payload)
        # print file.text #to test what the FB api responded with
        result = file.text.split("=")[1]
        # print file.text #to test the TOKEN
        return result

    def post_facebook(self, access_token):
        graph = facebook.GraphAPI(access_token)
        profile = graph.get_object("me")
        friends = graph.get_connections("me", "friends")

        friend_list = [friend['name'] for friend in friends['data']]

        print friend_list
