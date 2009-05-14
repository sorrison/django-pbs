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
from django.http import HttpResponse, Http404
from django_pbs.jobs.models import Job
from django_pbs.servers.models import Server
from django_pbs import serializers

def job_detail(request, job_id, server_id=None, xml=False):

    
    id, server = job_id.split('.', 1)

    try:
        job = Job(Server(server), id)
    except:
        raise Http404

    if xml:
        return HttpResponse(serializers.serialize('xml', [job], indent=True), mimetype='text/xml')

    return render_to_response('pbs_jobs/job_detail.html', locals(), context_instance=RequestContext(request))
