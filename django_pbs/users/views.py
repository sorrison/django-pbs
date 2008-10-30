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

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django_pbs.servers.models import Server, Queue



def user_detail(request, username):

    job_list = []

    for s in settings.LOCAL_PBS_SERVERS:
        try:
            server = Server(s)
            job_list.extend(server.job_list([username]))
        except:
            pass

    return render_to_response('pbs_users/user_detail.html', locals(), context_instance=RequestContext(request))

