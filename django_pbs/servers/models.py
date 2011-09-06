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

from PBSQuery import PBSQuery
from django_pbs.jobs.models import Job


class Server(object):

    def __init__(self, server_name):
        p = PBSQuery(str(server_name))
        info = p.get_serverinfo().items()[0]
        self.name = info[0]
        self.p = p
        for k,v in info[1].items():
            if k.startswith('resources'):
                for i,j in v.items():
                    setattr(self, k + '_' + i, j[0])
            else:
                setattr(self, k, v[0]) 

    def __str__(self):
        return self.name

    def _get_pk_val(self):
        return self.name

    def get_absolute_url(self):
        return '/servers/%s/' % self.name
        
    def getnodes(self):
        return self.p.getnodes()

    def getqueues(self):
        return self.p.getqueues()

    def getjobs(self):
        return self.p.getjobs()

    def getjob(self, id):
        return self.p.getjob(id)

    def cpu_stats(self):
        node_data = self.getnodes()
        total = 0
        used = 0
        for k, n in node_data.items():
            if 'cluster' not in n['ntype']:
                continue
            if 'offline' in n['state'] or 'down' in n['state']:
                continue
            total += int(n['np'][0])
            try:
                used += len(n['jobs'])
            except:
                pass
        return used,total
        

    def job_list(self, usernames=None):
        data_list = self.getjobs()
        job_list = []
        for d in data_list:
            id, host = d.split('.', 1)
            if usernames:
                owner, host = data_list[d]['Job_Owner'][0].split('@')
                if owner in usernames:
                    job_list.append(Job(server=self, id=id, data=data_list[d]))
            else:
                job_list.append(Job(server=self, id=id, data=data_list[d]))
        return job_list

    def node_list(self):
        data = self.getnodes()
        nodes = []
        for k,v in data.items():
            v = dict(v)
            nodes.append(Node(self, k, v))
        return nodes
                         
    def queue_list(self):
        data = self.getqueues()
        queues = []
        for k,v in data.items():
            queues.append(Queue(self, k, dict(v)))
        return queues


class Queue:

    def __init__(self, server, name, data=None):

        self.server = server
        self.name = str(name)
        
        if not data:
            data = self.server.p.getqueue(self.name)
            
        for k,v in data.items():
            if k.startswith('resources'):
                for i,j in v.items():
                    setattr(self, k + '_' + i, j[0])
            else:
                setattr(self, k, v[0])

    def __str__(self):
        return self.name

    def _get_pk_val(self):
        return self.name
    
    def get_absolute_url(self):
        return '/servers/%s/queues/%s/' % (self.server, self.name)
    
    
        
class Node:

    def __init__(self, server, name, data=None):

        self.server = server
        self.name = str(name)

        if not data:
            data = self.server.p.getnode(self.name)
        
        self.type = data['ntype'][0]
        self.np = int(data['np'][0])

        if 'jobs' in data:
            self.np_used = len(data['jobs'])
        else:
            self.np_used = 0

        if 'free' in data['state'] and 'jobs' in data:
            self.state = 'partial'
        else:
            self.state = data['state'][0]
        self.jobs = data.get('jobs', None)
        try:
            self.note = data['note'][0]
        except KeyError:
            self.note = ''
        #self.job_list = self.get_job_list()
        
    def __str__(self):
        return self.name

    def _get_pk_val(self):
        return self.name

    def is_free(self):
        if self.state == 'free':
            return True
        return False

    def is_online(self):
        if state == 'down' or state == 'offline':
            return False
        return True
    
    def get_job_list(self):
        job_list = []

        if not self.jobs:
            return job_list
        for j in self.jobs:

            full_id = j[j.index('/')+1:]
            id, host = full_id.split('.', 1)
            job_list.append(Job(server=self.server, id=id, full_id=full_id))
                

        return job_list

    def get_absolute_url(self):
        return '/servers/%s/nodes/%s/' % (self.server, self.name)
        


        
