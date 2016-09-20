
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from site import urls as site_urls
from administation import urls as admin_urls

urlpatterns = [
    url(r'^root/', include(admin.site.urls)),
    # url(r'^admin/', include(admin_urls)),
    # url(r'^', include(site_urls)),
    # url(r'^tinymce/', include('tinymce.urls')),
    # authentication
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'administration/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^thumbnails/', include('imagefit.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin_urls)),
    url(r'^', include(site_urls)),

    url(r'^tinymce/', include('tinymce.urls')),
)
