from django.conf.urls import patterns, url
from kibaru.administation import views


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^add_article', views.add_article, name='add_article'),
                       )
