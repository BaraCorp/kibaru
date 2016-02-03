#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import oauth2
import twitter
import urllib
import urllib2
from django.conf import settings


def post_to_twitter(sender, instance, *args, **kwargs):
    """
    Post new saved objects to Twitter.
    """

    TWITTER_MAXLENGTH = getattr(settings, 'TWITTER_MAXLENGTH', 140)

    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET
    access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
    domain = settings.DOMMAIN
    http_headers = None

    if not instance.twitte:
        print("Not Twitte ", instance.twitte)
        return
    # url = instance.get_absolute_url()
    url = instance.get_short_id
    prefix_url_twtt = instance.prefix_url_twtt
    if not url.startswith('http://') and not url.startswith('https://'):
        url = u'%s/%s/%s' % (domain, prefix_url_twtt, url)
    print(url)
    # TODO
    # tinyurl'ze the object's link
    # create_api = 'http://tinyurl.com/api-create.php'
    # data = urllib.urlencode(dict(url=url))
    # link = urllib2.urlopen(create_api, data=data).read().strip()
    link = url
    try:
        text = instance.get_twitter_message()
    except AttributeError:
        text = unicode(instance)
    # instance.delete()

    mesg = join_(text, link)
    if len(mesg) > TWITTER_MAXLENGTH:
        size = len(mesg + '...') - TWITTER_MAXLENGTH
        mesg = join_(text[:-size], link)
    try:
        # Autant twitter
        consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth2.Token(key=access_token_key, secret=access_token_secret)
        client = oauth2.Client(consumer, token)

        url_twitter = "https://api.twitter.com/1.1/statuses/update.json?",
        body = urllib.urlencode({"status": str(mesg), "wrap_links": True})
        if not settings.DEBUG:
            resp, content = client.request(
                "https://api.twitter.com/1.1/statuses/update.json?", method="POST", body=body, headers=http_headers)
            print("{} Send twitter".format(resp))
        else:
            print("Not POST on Twitter")
    except oauth2.Error as err:
        print("Twitter Error:" + err)
    except Exception as e:
        print(e)


def join_(a, b):
    return u' '.join((a, b)).encode('utf-8')
