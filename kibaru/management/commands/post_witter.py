#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os

from TwitterAPI import TwitterAPI

from django.conf import settings
from django.core.management.base import BaseCommand


from kibaru.models import Article


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
            print(url_img)
            file = open(url_img, 'rb')
            media.update({'media[]': file.read()})
        # print(data)
        # self.twitter(data, media)

    def twitter(self, data, media):
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        domain = settings.DOMMAIN

        api = TwitterAPI(consumer_key, consumer_secret, access_token_key,
                         access_token_secret)
        r = api.request(
            'statuses/update_with_media', data, media)
        # print(r.status_code)
