#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import short_url

from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse
from kibaru.models import (Article, Publicity, Category, New, Video, Language,
                           Directory, Job)
from kibaru.forms import Newsletterform
from django.conf import settings
from kibaru.site.search import get_query

NOW = datetime.now()
MONTH_NAMES = ('', _('January'), _('February'), _('March'), _('April'),
               _('May'), _('June'), _('July'), _('August'), _('September'),
               _('October'), _('November'), _('December'))


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def year_view(request, year):
    posts, context = init(year=year)
    for article in posts:
        article.url_display = reverse("art", args=[article.slug])
    context.update({'post_list': posts, "lang": request.LANGUAGE_CODE,
                    'subtitle': '{} {}'.format(_("The articles published in"),
                                               year)})
    return render(request, 'site/list_page.html', context)


def month_view(request, year, month):
    posts, context = init(month=month, year=year)
    for article in posts:
        article.url_display = reverse("art", args=[article.slug])
    context.update({'post_list': posts, "lang": request.LANGUAGE_CODE,
                    'subtitle': "{} {} {}".format(_("The articles published in"),
                                                  MONTH_NAMES[int(month)], year),
                    })
    return render(request, 'site/list_page.html', context)


# def tag_view(request, tag):
#     allposts, context = init()
#     posts = []
#     for post in allposts:
#         post.url_display_tag = reverse("art", args=[post.slug])
#         tags = re.split(' ', post.tags)
#         if tag in tags:
#             posts.append(post)
#     context.update({'post_list': posts,
#                     'subtitle': "Articles tagged '%s'" % tag, })
#     return render(request, 'site/search_results.html', context)


def init(lang='fr', month=None, year=None, cat_slug=None):

    current_lang = Language.objects.get(slug=lang)
    posts = Article.objects.filter(lang=current_lang, status=Article.POSTED)
    archive_data = create_archive_data(posts)
    articles = posts
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

    jobs = Job.objects.filter(date_expired__gte=datetime.today, lang=current_lang)
    for job in jobs:
        job.url_display = reverse("display_job", args=[job.id])

    for publicity in publicities:
        publicity.url_display = reverse("display_publicity", args=[publicity.id])
    free_expressions = articles.filter(
        category=Category.objects.get(slug="expression-libre")
        )[:4] if not cat_slug == "expression-libre" else []
    for free_expression in free_expressions:
        free_expression.url_display = reverse(
            "art", args=[free_expression.slug])

    migrations = articles.filter(category=Category.objects.get(slug="migration"))[
        :4] if not cat_slug == "migration" else []
    for migration in migrations:
        migration.url_display = reverse("art", args=[migration.slug])

    sports = articles.filter(category=Category.objects.get(slug="sport"))[
        :3] if not cat_slug == "sport" else []
    for sport in sports:
        sport.url_display = reverse("art", args=[sport.slug])

    art_cultures = articles.filter(category=Category.objects.get(slug="culture"))[
        :4] if not cat_slug == "culture" else []
    for culture in art_cultures:
        culture.url_display = reverse("art", args=[culture.slug])
    starts = posts.filter(start=True)[:5]
    for start in starts:
        start.url_display = reverse("art", args=[start.slug])

    news = New.objects.filter(lang=current_lang,)
    # start_dat = datetime(NOW.year, NOW.month, NOW.day)
    # end_dat = start_dat + timedelta(days=1)
    # news_today = news.filter(date__gte=start_dat, date__lte=end_dat)
    # if news_today.count() > 0:
    # news = news_today
    # else:
    # news = news[:5]
    for new in news:
        new.url_display = reverse("news", args=[new.id])
    # tag_data = create_tag_data(posts)
    context = {'settings': settings,
               'flash_news': news,
               'post_list': posts,
               'art_cultures': art_cultures,
               'art_culture_title': _("Art and Culture"),
               'sports': sports,
               'sport_title': _("Sport"),
               'migrations': migrations,
               'migration_title': _("migration"),
               'free_expressions': free_expressions,
               'free_expression_title': _("Free Expression"),
               # 'tag_counts': tag_data,
               'archive_counts': archive_data,
               'publicities': publicities,
               'jobs': jobs,
               'job_title': _("Avis"),
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
    posts, context = init(lang=request.LANGUAGE_CODE)
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        article_query = get_query(query_string, ['title', 'text',])
        found_article = posts.filter(article_query)

    for article in found_article:
        article.url_display = reverse("art", args=[article.slug])
    context.update({'query_string': query_string, "lang": request.LANGUAGE_CODE,
                    'found_article': found_article})
    return render(request, 'site/search_results.html', context)


def home(request, *args, **kwargs):
    cat_slug = kwargs["slug"]

    try:
        slug = Category.objects.get(slug=cat_slug).slug
        posts, context = init(lang=request.LANGUAGE_CODE, cat_slug=slug)
    except Category.DoesNotExist:
        posts, context = init(lang=request.LANGUAGE_CODE, cat_slug=None)
        posts = posts.exclude(
            category=Category.objects.get(slug="expression-libre")).exclude(
            category=Category.objects.get(slug="migration")).exclude(
            category=Category.objects.get(slug="sport")).exclude(
            category=Category.objects.get(slug="culture"))
        slug = None
    for article in posts:
        article.url_display = reverse("art", args=[article.slug])
    starts = posts.filter(start=True)[:5]
    for start in starts:
        start.url_display = reverse("art", args=[start.slug])

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
            messages.success(request, _("Thank you for your subscription"))
            return HttpResponseRedirect('/')
    else:
        form = Newsletterform()
    context.update({'posts': posts, 'form': form, 'subtitle': '',
                    "starts": starts, "cat_slug": cat_slug, "lang": request.LANGUAGE_CODE})
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

    posts, context = init(lang=request.LANGUAGE_CODE)
    article_slug = kwargs["slug"]
    try:
        if len(article_slug) < 9:
            article = posts.get(id=short_url.decode_url(article_slug))
        else:
            article = posts.get(slug=article_slug)
    except Article.DoesNotExist:
        raise Http404(_("Article does not exist"))
        return HttpResponseRedirect('/' + request.LANGUAGE_CODE + '/')
    article.short_url = reverse("art", args=[article.get_short_id])
    article.count_view += 1
    article.save()
    context.update({'article': article, "lang": request.LANGUAGE_CODE})
    return render(request, 'site/article_detail.html', context)

def about(request, *args, **kwargs):
    if request.LANGUAGE_CODE == "ar":
        filename =  settings.AR_LEDIT
    else:
        filename =  settings.FR_LEDIT

    # with open(filename) as pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(_("Ligne editoriale du site"))
    #     return response

    return render(request, 'site/about.html', {'url_pdf' : filename})

def display_new(request, *args, **kwargs):
    posts, context = init()
    new_id = kwargs["id"]
    new = New.objects.get(id=new_id)
    new.count_view += 1
    new.save()
    context.update({'new': new, "lang": request.LANGUAGE_CODE})
    return render(request, 'site/new_detail.html', context)


def display_publicity(request, *args, **kwargs):
    context = {}
    publicity_id = kwargs["id"]
    publicity = Publicity.objects.get(id=publicity_id)

    context.update({'publicity': publicity, "lang": request.LANGUAGE_CODE})
    return render(request, 'site/display_publicity.html', context)


def display_job(request, *args, **kwargs):
    posts, context = init()
    job_id = kwargs["id"]
    job = Job.objects.get(id=job_id)
    job.count_view += 1
    job.save()
    context.update({'job': job, "lang": request.LANGUAGE_CODE})
    # return render(request, 'site/display_job.html', context)
    #Avis de manifestation d'interet - MEP  Reinsertion Project Mali_14.03.2017
    # filename= "Avis-de-manifestation-d'interet-MEP-Reinsertion-Project-Mali_14.03.2017.pdf"
    # return render(request, 'site/about.html', {'url_pdf' : filename})
    return render(request, 'site/display_job.html', context)


def notices(request, *args, **kwargs):
    posts, context = init()
    notices = Job.objects.all()
    context.update({'notices': notices, "lang": request.LANGUAGE_CODE})
    return render(request, 'site/notices.html', context)


def display_videos(request, *args, **kwargs):
    posts, context = init()

    context.update({'posts': posts, "lang": request.LANGUAGE_CODE})
    return render(request, 'site/videos.html', context)


def display_heading(request, *args, **kwargs):
    posts, context = init()

    sports = posts.filter(category=Category.objects.get(slug="sport"))[:3]
    context.update({'sports': sports,
                    'posts': posts, "lang": request.LANGUAGE_CODE})
    return render(request, 'site/videos.html', context)


def directory(request, *args, **kwargs):
    posts, context = init()
    directories = Directory.objects.all()
    context.update(
        {'subtitle': 'Presse Malienne', 'directories': directories, 'posts': posts, "lang": request.LANGUAGE_CODE})
    return render(request, 'site/directory.html', context)
