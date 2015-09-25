from django.shortcuts import render
from django.core.urlresolvers import reverse

from kibaru.models import Article, Publicity


def home(request):
    context = {}
    articles = Article.objects.all()
    publicities = Publicity.objects.all()

    for article in articles:
        article.url_display = reverse("display_article", args=[article.id])

    for publicity in publicities:
        publicity.url_display = reverse("display_publicity", args=[publicity.id])
    context.update({'articles': articles, 'publicities': publicities})

    print(context)
    # return HttpResponse("Hello, world. You're at the site home.")
    return render(request, 'site/index.html', context)


def display_article(request, *args, **kwargs):
    context = {}
    article_id = kwargs["id"]
    article = Article.objects.get(id=article_id)

    context.update({'article': article})
    return render(request, 'site/article_detail.html', context)


def display_publicity(request, *args, **kwargs):
    context = {}
    publicity_id = kwargs["id"]
    publicity = Publicity.objects.get(id=publicity_id)

    context.update({'publicity': publicity})
    return render(request, 'site/display_publicity.html', context)
