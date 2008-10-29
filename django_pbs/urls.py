from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',

    url(r'^$', 'django_pbs.servers.views.server_list'),                    
    url(r'^servers/', include('django_pbs.servers.urls')),
    url(r'^xml/servers/', include('django_pbs.servers.urls'), {'xml': True}),
    url(r'^jobs/', include('django_pbs.jobs.urls')),
    url(r'^xml/jobs/', include('django_pbs.jobs.urls'), {'xml': True}),
    url(r'^users/', include('django_pbs.users.urls')),
    url(r'^moab/', include('django_pbs.moab.urls')),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^pbs_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )		
