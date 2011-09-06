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

from django.db import models
import datetime
from decimal import Decimal


def get_in_seconds(time):
    """
    Takes a string in format HH:MM:SS
    Note hours can be more than 2 digits

    if greater than 3 years
    
    returns the time in seconds
    """

    if time is None:
        return 0

    hours, minutes, seconds = time.split(':')


    #26280 = 3 years in hours
    if int(hours) > 26280:
        raise ValueError

    total = (Decimal(hours)*60*60) + (Decimal(minutes)*60) + Decimal(seconds)

    return total



class Job(object):

    def __init__(self, server, id, full_id=None, data=None):

        self.server = server
        self.id = str(id)

        if full_id is None:
            self.full_id = '%s.%s' % (self.id, self.server)
        else:
            self.full_id = full_id

        if data is None:
            data = self.server.getjob(self.full_id)

        for k,v in data.items():
            if k.startswith('Resource') or k.startswith('resources') or k.startswith('Walltime'):
                for i,j in v.items():
                    setattr(self, k + '_' + i, j[0])
            else:
                setattr(self, k, v[0]) 

        self.server = server
        self.username = self.Job_Owner.split('@')[0]

        state_map = {
            'R': 'Running',
            'Q': 'Queued',
            'E': 'Exiting',
            'H': 'Held',
            'B': 'Blocked',
            }
        try:
            self.state = state_map[self.job_state]
        except:
            self.state = self.job_state

        self.est_walltime = self.Resource_List_walltime
        try:
            self.count = self.Resource_List_nodes
        except:
            pass
        self.mtime = datetime.datetime.fromtimestamp(int(self.mtime))
        self.qtime = datetime.datetime.fromtimestamp(int(self.qtime))
        self.ctime = datetime.datetime.fromtimestamp(int(self.ctime))
        try:
            self.cpus_used = self.Resource_List_nodect
        except:
            pass

        try:
            self.etime = datetime.datetime.fromtimestamp(int(self.etime))
        except:
            self.etime = None

        self.walltime = get_in_seconds(self.est_walltime)
        try:
            self.act_walltime = self.resources_used_walltime
            self.running_time = get_in_seconds(self.act_walltime)
        except:
            pass
        try:
            self.submission_host = self.Output_Path.split(':')[0]
        except:
            self.submission_host = None

    def __str__(self):
        return self.full_id

    def _get_pk_val(self):
        return self.full_id

    def node_list(self):
        hosts = self.exec_host
        hosts = hosts.split('+')
        node_list = []
        for n in hosts:
            try:
                node_list.append(n[:n.index('/')])
            except:
                pass
        return node_list
    
 
    def percent_remaining(self):
        return (get_in_seconds(self.act_walltime  ) / get_in_seconds(self.est_walltime  )) * 100


    def remaining(self):
        return int(self.Walltime_Remaining)
        

    def start(self):
        if self.state == 'Running':
            return datetime.datetime.now() - datetime.timedelta(seconds=int(self.running_time))
        else:
            return None
    
    def waiting(self):
        if self.state == 'Queued' or self.state == 'Blocked':
            delta = datetime.datetime.now() - self.qtime
            return int((delta.days*3600) + delta.seconds)
        else:
            return ''


    def get_absolute_url(self):
        return '/jobs/%s/' % self.full_id
