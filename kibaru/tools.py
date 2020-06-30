#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os

import html2text
from TwitterAPI import TwitterAPI

from django.conf import settings

import facebook


TWITTER_MAXLENGTH = getattr(settings, 'TWITTER_MAXLENGTH', 140)


def get_text_in_html(htext):
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(htext)


def full_image_url(img_name):
    return


def social_share(sender, instance, *args, **kwargs):
    if instance.twitter:
        post_to_twitter(sender, instance)
        post_to_facebook(sender, instance)


def post_to_facebook(sender, instance):
    image_path = ""
    caption = ""
    if sender.__name__ == "New":
        caption = instance.TYPE_NEWS_CHOICES.get(instance.type_new)

    if sender.__name__ == "Article":
        caption = instance.category.name
        if instance.image:
            image_path = instance.image.name

    # attach = {
    #     "name": u"{}".format(settings.APP_NAME),
    #     "link": instance.post_url(),
    #     "page_token": settings.PAGE_TOKEN,
    #     "description": u"{}".format(caption),
    #     # "picture": os.path.join(settings.DOMMAIN, "media", image_path),
    #     "caption": u"{}".format(caption)
    # }

    msg = u"{}".format(instance.title)
    graph = facebook.GraphAPI(access_token=settings.PAGE_TOKEN)

    graph.put_object(
       parent_object=settings.FACEBOOK_PAGE_ID,
       connection_name="feed",
       message=msg,
       link=instance.post_url()
    )

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
