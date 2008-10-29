from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django_pbs.jobs.models import Job
from django_pbs.servers.models import Server
from django_pbs import serializers

def job_detail(request, job_id, server_id=None, xml=False):

    
    id, server = job_id.split('.', 1)

    job = Job(Server(server), id)


    if xml:
        return HttpResponse(serializers.serialize('xml', [job], indent=True), mimetype='text/xml')

    return render_to_response('pbs_jobs/job_detail.html', locals(), context_instance=RequestContext(request))
