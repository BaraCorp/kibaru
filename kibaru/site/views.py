#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import re

from django.shortcuts import render
from django.core.urlresolvers import reverse

from datetime import datetime
from django.shortcuts import render_to_response

from kibaru.models import Article, Publicity
from django.conf import settings

MONTH_NAMES = ('', 'Janvier', u'Février', 'Mars', 'Avril', 'peut', 'Juin',
               'Juillet', u'Août', 'Septembre', 'Octobre', 'Novembre', u'Décembre')


def single_post(request, year, month, slug2):
    posts, context = init()
    post = posts.get(date_created__year=year,
                     date_created__month=int(month),
                     slug=slug2,)
    context.update({'post': post})
    print(posts)
    return render('site/single_post.html', context)


def year_view(request, year):
    print("year_view")
    posts, context = init(year=year)
    context.update({'post_list': posts,
                    'subtitle': 'Articles for %s' % year})
    return render(request, 'site/list_page.html', context)


def month_view(request, year, month):
    posts, context = init(month=month, year=year)
    context.update({'post_list': posts,
                    'subtitle': 'Articles for %s %s' % (MONTH_NAMES[int(month)], year), })
    return render(request, 'site/list_page.html', context)


def tag_view(request, tag):
    print("tagview")
    allposts, context = init()
    posts = []
    for post in allposts:
        post.url_display_tag = reverse("display_article", args=[post.slug])
        tags = re.split(' ', post.tags)
        if tag in tags:
            posts.append(post)
    context.update({'post_list': posts,
                    'subtitle': "Articles tagged '%s'" % tag, })
    return render(request, 'site/list_page.html', context)


def init(month=None, year=None):
    print("init")
    posts = Article.objects.all()

    if month:
        posts = posts.filter(
            date_created__year=year, date_created__month=int(month))
    elif year:
        posts = posts.filter(date_created__year=year)

    for article in posts:
        article.url_display = reverse("display_article", args=[article.slug])

    tag_data = create_tag_data(posts)
    archive_data = create_archive_data(posts)
    context = {'settings': settings,
               'post_list': posts,
               'tag_counts': tag_data,
               'archive_counts': archive_data, }
    return posts, context


def create_archive_data(posts):
    archive_data = []
    count = {}
    mcount = {}
    for post in posts:
        year = post.date_created.year
        month = post.date_created.month
        if year not in count:
            count[year] = 1
            mcount[year] = {}
        else:
            count[year] += 1
        if month not in mcount[year]:
            mcount[year][month] = 1
        else:
            mcount[year][month] += 1
    for year in sorted(count.iterkeys(), reverse=True):
        archive_data.append({'isyear': True,
                             'year': year,
                             'count': count[year], })
        for month in sorted(mcount[year].iterkeys(), reverse=True):
            archive_data.append({'isyear': False,
                                 'yearmonth': '%d/%02d' % (year, month),
                                 'monthname': MONTH_NAMES[month],
                                 'count': mcount[year][month], })
    return archive_data


def create_tag_data(posts):
    tag_data = []
    count = {}
    for post in posts:
        tags = re.split(" ", post.tags)
        for tag in tags:
            if tag not in count:
                count[tag] = 1
            else:
                count[tag] += 1
    for tag, count in sorted(count.iteritems(), key=lambda(k, v): (v, k), reverse=True):
        tag_data.append({'tag': tag,
                         'count': count, })
    return tag_data


def home(request):
    context = {}
    # articles = Article.objects.all()
    publicities = Publicity.objects.all()

    posts, context = init()
    context.update({'subtitle': '', })

    for publicity in publicities:
        publicity.url_display = reverse(
            "display_publicity", args=[publicity.id])
    context.update({'articles': posts, 'publicities': publicities})
    return render(request, 'site/index.html', context)


def display_article(request, *args, **kwargs):
    context = {}
    article_slug = kwargs["slug"]
    article = Article.objects.get(slug=article_slug)

    context.update({'article': article})
    return render(request, 'site/article_detail.html', context)


def display_publicity(request, *args, **kwargs):
    context = {}
    publicity_id = kwargs["id"]
    publicity = Publicity.objects.get(id=publicity_id)

    context.update({'publicity': publicity})
    return render(request, 'site/display_publicity.html', context)
