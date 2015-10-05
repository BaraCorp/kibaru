from django.conf.urls import patterns, url
from kibaru.administation import views


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^add_article/$', views.add_article, name='add_article'),
                       url(r'^edit_article/(?P<id>\d+)$', views.edit_article, name='edit_article'),
                       url(r'^del_article/(?P<id>\d+)$', views.del_article, name="del_article"),
                       )
