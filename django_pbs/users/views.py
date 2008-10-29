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

