#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os

from TwitterAPI import TwitterAPI
from django.conf import settings

TWITTER_MAXLENGTH = getattr(settings, 'TWITTER_MAXLENGTH', 140)


def get_body_twitte(body):
    text, url = body
    msg = join_(text, url)
    if len(msg) > TWITTER_MAXLENGTH:
        size = len(msg.decode('utf-8') + '...') - TWITTER_MAXLENGTH
        msg = join_(text[:-size], url)
    return msg


def post_to_twitter(sender, instance, *args, **kwargs):
    """
    Post new saved objects to Twitter.
    """

    if instance._state.adding and instance.status == instance.POSTED:
        print("Not Twitte ", instance.twitte)
        return
    if settings.DEBUG == True:
        return

    data = {"status": str(get_body_twitte(instance.get_twitter_message()))}
    media = {}

    tw_url = 'statuses/update'
    image = instance.image
    if image:
        file = open(os.path.join(settings.MEDIA_ROOT, image.name), 'rb')
        media.update({'media[]': file.read()})
        tw_url = 'statuses/update_with_media'

    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET
    access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    api = TwitterAPI(
        consumer_key, consumer_secret, access_token_key, access_token_secret)
    r = api.request(tw_url, data, media)
    # print(r.status_code)


def join_(a, b):
    return u' '.join((a, b)).encode('utf-8')
