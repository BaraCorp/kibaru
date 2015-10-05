from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from kibaru.form import Articleform
from kibaru.models import Article, Member, Category


@login_required()
def home(request):
    context = {}
    articles = Article.objects.all().order_by('date_created')
    for article in articles:
        article.url_edit = reverse("edit_article", args=[article.id])
        article.url_del = reverse("del_article", args=[article.id])
    context.update({'articles': articles})
    return render(request, 'administration/index.html', context)


@login_required
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


@login_required()
def edit_article(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected_article = Article.objects.get(id=id_url)
    if request.method == 'POST':
        form = Articleform(request.POST, request.FILES, instance=selected_article)
        if form.is_valid():
            selected_article.title = request.POST.get('title')
            selected_article.text = request.POST.get('text')
            if request.FILES.get('image'):
                selected_article.image = request.FILES.get('image')
            selected_article.author = Member.objects.get(username=request.POST.get('author'))
            selected_article.category = Category.objects.get(slug=request.POST.get('category'))
            selected_article.status = request.POST.get('status')

            form.save()
            messages.success(request, u"L'article")
            return HttpResponseRedirect('/admin/')

    else:
        form = Articleform(instance=selected_article)
    return render(request, 'administration/add_article.html', {'form': form, 'page_title': "Modification d'article"})


@login_required
def del_article(request, *args, **kwargs):
    id_url = kwargs["id"]
    selected = Article.objects.get(id=id_url)
    selected.delete()
    messages.success(request, u"L'article a ete supprime")
    return redirect('/admin/')
