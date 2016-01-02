#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from kibaru.forms import Articleform, Newform, Videoform
from kibaru.models import Article, Member, Category, New, Video


@login_required()
def home(request):
    context = {}

    articles = Article.objects.all().order_by('-date_created')
    paginator = Paginator(articles, 4)
    page = request.GET.get('page')

    news = New.objects.all().order_by('-date')
    paginator1 = Paginator(news, 4)
    page1 = request.GET.get('page1')

    videos = Video.objects.all().order_by('-date_created')
    paginator2 = Paginator(videos, 4)
    page2 = request.GET.get('page2')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    try:
        news = paginator1.page(page1)
    except PageNotAnInteger:
        news = paginator1.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator1.page(paginator.num_pages)

    try:
        videos = paginator2.page(page2)
    except PageNotAnInteger:
        videos = paginator2.page(1)
    except EmptyPage:
        videos = paginator2.page(paginator.num_pages)

    for article in articles:
        article.url_edit = reverse("edit_article", args=[article.id])
        article.url_del = reverse("del_article", args=[article.id])
    str_news = ""
    for new in news.object_list:
        new.url_edit = reverse("edit_new", args=[new.id])
        new.url_del = reverse("del_new", args=[new.id])
        str_news += "{} | {}; ".format(new.title, new.comment)

    for video in videos:
        video.url_del = reverse("del_video", args=[video.id])

    context.update({'articles': articles, 'news': news,
                    'videos': videos, 'str_news': str_news})
    return render(request, 'administration/index.html', context)


# @login_required
def add_article(request):
    c = {'page_title': "Ajout d'article"}
    if request.method == 'POST':
        form = Articleform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, u"l'article a ete ajouter")
            return HttpResponseRedirect('/admin/')
    else:
        form = Articleform()
    c.update({'form': form})
    return render(request, 'administration/add_article.html', c)


# @login_required
def add_new(request):
    c = {'page_title': "Ajout de nouvelle"}
    if request.method == 'POST':
        form = Newform(request.POST, request.FILES)
        if form.is_valid():
            request.date = datetime(form.cleaned_data.get('date').year,
                                    form.cleaned_data.get('date').month,
                                    form.cleaned_data.get('date').day)
            form.save()
            messages.success(request, u"la nouvelle a ete ajouter")
            return HttpResponseRedirect('/admin/')
    else:
        form = Newform()
    c.update({'form': form})
    return render(request, 'administration/add_new.html', c)


# @login_required
def add_video(request):
    c = {'page_title': "Ajout de lien d'une video Youtube"}
    if request.method == 'POST':
        form = Videoform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u"le lien de la video a ete ajouter")
            return HttpResponseRedirect('/admin/')
    else:
        form = Videoform()
    c.update({'form': form})
    return render(request, 'administration/add_video.html', c)


# @login_required()
def edit_article(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected_article = Article.objects.get(id=id_url)
    if request.method == 'POST':
        form = Articleform(request.POST, request.FILES,
                           instance=selected_article)
        if form.is_valid():
            # article = Article.objects.get(start=True)
            # article.start = False
            # article.save()
            selected_article.title = request.POST.get('title')
            selected_article.text = request.POST.get('text')
            if request.FILES.get('image'):
                selected_article.image = request.FILES.get('image')
            selected_article.author = Member.objects.get(
                username=request.POST.get('author'))
            selected_article.category = Category.objects.get(
                slug=request.POST.get('category'))
            selected_article.status = request.POST.get('status')

            form.save()
            messages.success(request, u"L'article a ete mise a jour")
            return HttpResponseRedirect('/admin/')

    else:
        form = Articleform(instance=selected_article)
    return render(request, 'administration/add_article.html',
                  {'form': form, 'page_title': "Modification d'article"})


# @login_required
def del_article(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected = Article.objects.get(id=id_url)
    selected.delete()
    messages.success(request, u"L'article a ete supprime")
    return redirect('/admin/')


# @login_required
def del_video(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected = Video.objects.get(id=id_url)
    selected.delete()
    messages.success(request, u"Le lien de la video a ete supprime")
    return redirect('/admin/')


# @login_required()
def edit_new(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected_new = New.objects.get(id=id_url)
    if request.method == 'POST':
        form = Newform(request.POST, instance=selected_new)
        if form.is_valid():
            selected_new.title = request.POST.get('title')
            selected_new.comment = request.POST.get('comment')
            selected_new.author = Member.objects.get(
                username=request.POST.get('author'))
            selected_new.date = datetime(form.cleaned_data.get('date').year,
                                         form.cleaned_data.get('date').month,
                                         form.cleaned_data.get('date').day,
                                         datetime.now().hour,
                                         datetime.now().minute,
                                         datetime.now().second)

            form.save()
            messages.success(request, u"La nouvelle a ete mise a jour")
            return HttpResponseRedirect('/admin/')

    else:
        form = Newform(instance=selected_new)
    return render(request, 'administration/add_new.html',
                  {'form': form, 'page_title': "Modification de la nouvelle"})


# @login_required
def del_new(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected = New.objects.get(id=id_url)
    selected.delete()
    messages.success(request, u"La nouvelle a ete supprime")
    return redirect('/admin/')
