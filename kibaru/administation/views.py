from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from kibaru.form import Articleform


def home(request):
    return HttpResponse("Hello, world. You're at the admin home.")


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
            return HttpResponseRedirect('/admin/add_article/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Articleform()
    return render(request, 'admin/add_article.html', {'form': form})
