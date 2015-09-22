from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


def home(request):
    # return HttpResponse("Hello, world. You're at the site home.")
    return render(request, 'site/index.html', {})
