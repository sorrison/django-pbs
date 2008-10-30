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

urlpatterns = patterns('django_pbs.servers.views',


    url(r'^$', 'server_list', name='pbs_server_list'),                     
    url(r'^(?P<server_id>[-.\w]+)/$', 'server_detail', name='pbs_server_detail'),
    url(r'^(?P<server_id>[-.\w]+)/queues/$', 'queue_list', name='pbs_queue_list'),
    url(r'^(?P<server_id>[-.\w]+)/queues/(?P<queue_id>[-.\w]+)/$', 'queue_detail', name='pbs_queue_detail'),
    url(r'^(?P<server_id>[-.\w]+)/nodes/$', 'node_list', name='pbs_node_list'),
    #(r'^(?P<server_id>[-.\w]+)/nodes/(?P<node_id>[-.\w]+)/$', 'node_detail'),
)


urlpatterns += patterns('django_pbs.jobs.views',

    url(r'^jobs/(?P<job_id>[-.\w]+)/$', 'job_detail', name='pbs_job_detail'),
)

urlpatterns += patterns('django_pbs.users.views',

    url(r'^users/(?P<username>[-.\w]+)/$', 'user_detail', name='pbs_user_detail'),
)
