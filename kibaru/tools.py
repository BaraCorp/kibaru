#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os

from TwitterAPI import TwitterAPI

from django.conf import settings

import facebook


TWITTER_MAXLENGTH = getattr(settings, 'TWITTER_MAXLENGTH', 140)


def full_image_url(img_name):
    return os.path.join(settings.DOMMAIN, "media", img_name)


def social_share(sender, instance, *args, **kwargs):

    # if settings.DEBUG == True:
    #     return
    if instance.twitter:
        post_to_twitter(sender, instance)
        post_to_facebook(sender, instance)


def post_to_facebook(sender, instance):
    attach = {
        "name": instance.type_text(),
        "link": instance.post_url(),
        "caption": settings.APP_NAME,
        "page_token": settings.PAGE_TOKEN
    }

    if instance.image:
        attach.update({"picture": full_image_url(instance.image.name)})
    try:
        attach.update({"description": instance.legend})
    except Exception as e:
        print(e)
    msg = instance.title
    page_id = "1652451611660511"
    graph = facebook.GraphAPI(settings.PAGE_TOKEN)
    post = graph.put_wall_post(
        message=msg, attachment=attach, profile_id=page_id)
    if post:
        return 'posted'
    return "No post"


def get_body_twitte(body):
    text, url = body
    msg = join_(text, url)
    if len(msg) > TWITTER_MAXLENGTH:
        size = len(msg.decode('utf-8') + '...') - TWITTER_MAXLENGTH
        msg = join_(text[:-size], url)
    return msg


def post_to_twitter(sender, instance, *args, **kwargs):
    tw_url = 'statuses/update'
    media = {}
    try:
        image = instance.image
    except Exception as e:
        print(e)
        image = None
    if image:
        file = open(os.path.join(settings.MEDIA_ROOT, image.name), 'rb')
        media.update({'media[]': file.read()})
        tw_url = 'statuses/update_with_media'

    data = {"status": str(get_body_twitte(instance.get_twiter_message()))}
    api = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                     settings.TWITTER_CONSUMER_SECRET,
                     settings.TWITTER_ACCESS_TOKEN_KEY,
                     settings.TWITTER_ACCESS_TOKEN_SECRET)
    r = api.request(tw_url, data, media)
    # print(r.status_code)


def join_(a, b):
    return u' '.join((a, b)).encode('utf-8')
