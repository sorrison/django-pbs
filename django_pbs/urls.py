# Copyright 2008 VPAC
#
# This file is part of django-pbs.
#
# django-pbs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-pbs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-pbs  If not, see <http://www.gnu.org/licenses/>.

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
