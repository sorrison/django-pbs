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
