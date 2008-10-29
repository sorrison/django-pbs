from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django_pbs.moab.models import MoabServer
from django_pbs.moab.forms import ShowstartForm

def showstart(request):

    if request.method == 'POST':

        form = ShowstartForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            server = data['server']
            procs = data['procs']
            time = data['time']

            s = MoabServer(server)
            result = s.showstart(procs, time)

    else:
        form = ShowstartForm()

    return render_to_response('pbs_moab/showstart_form.html', locals(), context_instance=RequestContext(request))
