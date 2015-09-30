from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from kibaru.form import Articleform
from kibaru.models import Article


@login_required()
def home(request):
    context = {}
    articles = Article.objects.all().order_by('date_created')
    context.update({'articles': articles})
    return render(request, 'administration/index.html', context)


@login_required()
def add_article(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Articleform(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.success(request, u"L'article")
            return HttpResponseRedirect('/administration/add_article/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Articleform()
    return render(request, 'administration/add_article.html', {'form': form})
