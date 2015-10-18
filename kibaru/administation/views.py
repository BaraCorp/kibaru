#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from datetime import date

from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from kibaru.forms import Articleform, Newform
from kibaru.models import Article, Member, Category, New


@login_required()
def home(request):
    context = {}
    articles = Article.objects.all().order_by('-date_created')
    news = New.objects.all().order_by('-date')
    for article in articles:
        article.url_edit = reverse("edit_article", args=[article.id])
        article.url_del = reverse("del_article", args=[article.id])
    str_news = ""
    for new in news:
        new.url_edit = reverse("edit_new", args=[new.id])
        new.url_del = reverse("del_new", args=[new.id])
        str_news += "{} | {}; ".format(new.title, new.comment)
    context.update({'articles': articles, 'news': news, 'str_news': str_news})
    return render(request, 'administration/index.html', context)


# @login_required
def add_article(request):
    c = {'page_title': "Ajout d'article"}
    if request.method == 'POST':
        form = Articleform(request.POST, request.FILES)
        if form.is_valid():
            article = Article.objects.get(start=True)
            article.start = False
            article.save()
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
            request.date = date(form.cleaned_data.get('date').year,
                                form.cleaned_data.get('date').month,
                                form.cleaned_data.get('date').day)
            form.save()
            messages.success(request, u"la nouvelle a ete ajouter")
            return HttpResponseRedirect('/admin/')
    else:
        form = Newform()
    c.update({'form': form})
    return render(request, 'administration/add_new.html', c)


# @login_required()
def edit_article(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected_article = Article.objects.get(id=id_url)
    if request.method == 'POST':
        form = Articleform(request.POST, request.FILES, instance=selected_article)
        if form.is_valid():
            article = Article.objects.get(start=True)
            article.start = False
            article.save()
            selected_article.title = request.POST.get('title')
            selected_article.text = request.POST.get('text')
            if request.FILES.get('image'):
                selected_article.image = request.FILES.get('image')
            selected_article.author = Member.objects.get(username=request.POST.get('author'))
            selected_article.category = Category.objects.get(slug=request.POST.get('category'))
            selected_article.status = request.POST.get('status')

            form.save()
            messages.success(request, u"L'article a ete mise a jour")
            return HttpResponseRedirect('/admin/')

    else:
        form = Articleform(instance=selected_article)
    return render(request, 'administration/add_article.html', {'form': form, 'page_title': "Modification d'article"})


# @login_required
def del_article(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected = Article.objects.get(id=id_url)
    selected.delete()
    messages.success(request, u"L'article a ete supprime")
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
            selected_new.author = Member.objects.get(username=request.POST.get('author'))
            selected_new.date = date(form.cleaned_data.get('date').year,
                                     form.cleaned_data.get('date').month,
                                     form.cleaned_data.get('date').day)

            form.save()
            messages.success(request, u"La nouvelle a ete mise a jour")
            return HttpResponseRedirect('/admin/')

    else:
        form = Newform(instance=selected_new)
    return render(request, 'administration/add_new.html', {'form': form, 'page_title': "Modification de la nouvelle"})


# @login_required
def del_new(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected = New.objects.get(id=id_url)
    selected.delete()
    messages.success(request, u"La nouvelle a ete supprime")
    return redirect('/admin/')
