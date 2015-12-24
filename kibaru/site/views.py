#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
from datetime import datetime, timedelta
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponseRedirect

from kibaru.models import Article, Publicity, Category, New, Video
from kibaru.forms import Newsletterform
from django.conf import settings
from kibaru.site.search import get_query

MONTH_NAMES = ('', 'Janvier', u'Février', 'Mars', 'Avril', 'peut', 'Juin',
               'Juillet', u'Août', 'Septembre', 'Octobre', 'Novembre', u'Décembre')

NOW = datetime.now()


def year_view(request, year):
    posts, context = init(year=year)
    for article in posts:
        article.url_display = reverse("display_article", args=[article.slug])
    context.update({'post_list': posts,
                    'subtitle': 'Articles pour %s' % year})
    return render(request, 'site/list_page.html', context)


def month_view(request, year, month):
    posts, context = init(month=month, year=year)
    for article in posts:
        article.url_display = reverse("display_article", args=[article.slug])
    context.update({'post_list': posts,
                    'subtitle': 'Articles pour %s %s' % (MONTH_NAMES[int(month)], year), })
    return render(request, 'site/list_page.html', context)


# def tag_view(request, tag):
#     allposts, context = init()
#     posts = []
#     for post in allposts:
#         post.url_display_tag = reverse("display_article", args=[post.slug])
#         tags = re.split(' ', post.tags)
#         if tag in tags:
#             posts.append(post)
#     context.update({'post_list': posts,
#                     'subtitle': "Articles tagged '%s'" % tag, })
#     return render(request, 'site/search_results.html', context)


def init(month=None, year=None, cat_slug=None):
    posts = Article.objects.filter(status=Article.POSTED)
    archive_data = create_archive_data(posts)
    if cat_slug:
        posts = posts.filter(category__slug=cat_slug)
    publicities = Publicity.objects.all()
    videos = Video.objects.all()
    videos_home = videos[:3]

    if month:
        posts = posts.filter(
            date_created__year=year, date_created__month=int(month))
    elif year:
        posts = posts.filter(date_created__year=year)

    for publicity in publicities:
        publicity.url_display = reverse(
            "display_publicity", args=[publicity.id])

    news = New.objects.all()
    start_dat = datetime(NOW.year, NOW.month, NOW.day)
    end_dat = start_dat + timedelta(days=1)
    news_today = news.filter(date__gte=start_dat, date__lte=end_dat)
    if news_today.count() > 0:
        news = news_today
    else:
        news = news[:5]

    for new in news:
        new.url_display = reverse("display_new", args=[new.id])
    # tag_data = create_tag_data(posts)
    context = {'settings': settings,
               'flash_news': news,
               'post_list': posts,
               # 'tag_counts': tag_data,
               'archive_counts': archive_data,
               'publicities': publicities,
               'videos_home': videos_home,
               'videos': videos}
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
                                 'year': year,
                                 'month': month,
                                 'monthname': MONTH_NAMES[month],
                                 'count': mcount[year][month], })
    return archive_data


# def create_tag_data(posts):
#     tag_data = []
#     count = {}
#     for post in posts:
#         tags = re.split(" ", post.tags)
#         for tag in tags:
#             if tag not in count:
#                 count[tag] = 1
#             else:
#                 count[tag] += 1
#     for tag, count in sorted(count.iteritems(), key=lambda(k, v): (v, k), reverse=True):
#         tag_data.append({'tag': tag,
#                          'count': count, })
#     return tag_data


def search(request):
    query_string = ''
    found_article = None
    posts, context = init()
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        article_query = get_query(query_string, ['title', 'text', ])
        found_article = posts.filter(article_query)

    for article in found_article:
        article.url_display = reverse("display_article", args=[article.slug])
    context.update({'query_string': query_string,
                    'found_article': found_article})
    return render(request, 'site/search_results.html', context)


def home(request, *args, **kwargs):
    cat_slug = kwargs["slug"]
    try:
        slug = Category.objects.get(slug=cat_slug).slug
    except Category.DoesNotExist:
        slug = None
    posts, context = init(cat_slug=slug)
    for article in posts:
        article.url_display = reverse("display_article", args=[article.slug])

    starts = posts.filter(start=True)[:5]
    for start in starts:
        start.url_start_display = reverse("display_article", args=[start.slug])

    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context.update(get_paginator_context(paginator, page))
    if request.method == 'POST':
        form = Newsletterform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u"Merci pour ton abonnement")
            return HttpResponseRedirect('/')
    else:
        form = Newsletterform()

    context.update({'posts': posts, 'form': form, 'subtitle': '',
                    "starts": starts, "cat_slug": cat_slug, })
    return render(request, 'site/index.html', context)


def get_paginator_context(obj_pagina, page, range_gap=3):
    try:
        page = int(page)
    except Exception as e:
        page = 1
    try:
        paginator = obj_pagina.page(page)
    except Exception as e:
        paginator = obj_pagina.page(1)

    if page > 4:
        start = page - range_gap
        start_pt = True
    else:
        start = 1
        start_pt = False

    if page < obj_pagina.num_pages - range_gap:
        end = page + range_gap + 1
        end_pt = True
    else:
        end_pt = False
        end = obj_pagina.num_pages + 1
    context = {
        'page_range': range(start, end),
        'start_pt': start_pt,
        'end_pt': end_pt,
        'last_page': obj_pagina.num_pages,
    }

    return context


def display_article(request, *args, **kwargs):
    posts, context = init()
    article_slug = kwargs["slug"]
    article = posts.get(slug=article_slug)
    article.count_view += 1
    article.save()

    context.update({'article': article})
    return render(request, 'site/article_detail.html', context)


def display_new(request, *args, **kwargs):
    posts, context = init()
    new_id = kwargs["id"]
    new = New.objects.get(id=new_id)
    context.update({'new': new})
    return render(request, 'site/new_detail.html', context)


def display_publicity(request, *args, **kwargs):
    context = {}
    publicity_id = kwargs["id"]
    publicity = Publicity.objects.get(id=publicity_id)

    context.update({'publicity': publicity})
    return render(request, 'site/display_publicity.html', context)


def display_videos(request, *args, **kwargs):
    posts, context = init()

    context.update({'posts': posts})
    return render(request, 'site/videos.html', context)
