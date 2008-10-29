from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.conf import settings
from django_pbs.servers.models import Server, Queue
from django_pbs import serializers


def server_list(request, xml=False):
    
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
