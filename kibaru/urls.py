

from site import urls as site_urls

from administation import urls as admin_urls

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^root/', include(admin.site.urls)),
    # authentication
    url(r'^thumbnails/', include('imagefit.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin_urls)),
    url(r'^', include(site_urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'administration/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^poll', include('poll.urls')),
)
