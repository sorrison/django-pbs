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
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.urlresolvers import reverse
from django_pbs.servers.models import Server, Queue
from django_pbs import serializers


def server_list(request, xml=False):

    if len(LOCAL_PBS_SERVERS) == 1:
        return HttpResponseRedirect(reverse('pbs_server_detail', LOCAL_PBS_SERVERS[0]))


    server_list = settings.LOCAL_PBS_SERVERS


    return render_to_response('pbs_servers/server_list.html', locals(), context_instance=RequestContext(request))



def server_detail(request, server_id, xml=False):

    if not server_id in settings.LOCAL_PBS_SERVERS:
        raise Http404

    server = Server(server_id)

    c_used, c_total = server.cpu_stats()
    c_percent = (float(c_used)/float(c_total))*100.00

    if xml:
        return HttpResponse(serializers.serialize('xml', [server], indent=True), mimetype='text/xml')

    return render_to_response('pbs_servers/server_detail.html', locals(), context_instance=RequestContext(request))


def queue_list(request, server_id, xml=False):

    server = Server(server_id)

    if xml:
        return HttpResponse(serializers.serialize('xml', server.queue_list(), indent=True), mimetype='text/xml')

    return render_to_response('pbs_servers/queue_list.html', locals(), context_instance=RequestContext(request))

def queue_detail(request, server_id, queue_id, xml=False):
    
    server = Server(server_id)
    
    queue = Queue(server, queue_id)

    if xml:
        return HttpResponse(serializers.serialize('xml', [queue], indent=True), mimetype='text/xml')


    return render_to_response('pbs_servers/queue_detail.html', locals(), context_instance=RequestContext(request))


def node_list(request, server_id, xml=False):

    server = Server(server_id)

    if xml:
        return HttpResponse(serializers.serialize('xml', server.node_list, indent=True), mimetype='text/xml')


    return render_to_response('pbs_servers/node_list.html', locals(), context_instance=RequestContext(request))
