from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^church/', include('church.urls')),
    url(r'^staff/', include('church.staffurls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
         {'next_page': '/church/home'}), 
    (r'^accounts/login/$', 'django.contrib.auth.views.login', 
         {'template_name': 'admin/login.html'}), 
)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
