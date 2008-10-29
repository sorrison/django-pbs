from PBSQuery import PBSQuery
from django_pbs.jobs.models import Job


class Server(object):

    def __init__(self, server_name):
        p = PBSQuery(str(server_name))
        info = p.get_serverinfo().items()[0]
        self.name = info[0]
        self.p = p
        for k,v in info[1].items():
            setattr(self, k.replace('.', '_'), v)

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
            if n['ntype'] != 'cluster':
                continue
            if n['state'] == 'offline' or n['state'] == 'down,offline':
                continue
            total += int(n['np'])
            try:
                used += len(n['jobs'].split(','))
            except:
                pass

        return used,total
        

    def job_list(self, usernames=None):
        data_list = self.getjobs()
        job_list = []
        for d in data_list:
            id, host = d.split('.', 1)
            if usernames:
                owner, host = data_list[d]['Job_Owner'].split('@')
                if owner in usernames:
                    job_list.append(Job(server=self, id=id, data=data_list[d]))
            else:
                job_list.append(Job(server=self, id=id, data=data_list[d]))
        return job_list

    def node_list(self):
        data = self.getnodes()
        nodes = []
        for k,v in data.items():
            nodes.append(Node(self, k, v))
        return nodes
                         
    def queue_list(self):
        data = self.getqueues()
        queues = []
        for k,v in data.items():
            queues.append(Queue(self, k, v))
        return queues
                       

    #def queue_list(self):

    #    data_list = self.getqueues()
    #    queue_list = []
    #    for d in data_list:
    #        queue_list.append(Queue(server=self, name=d, data=data_list[d]))

    #    return queue_list



class Queue:

    def __init__(self, server, name, data=None):

        self.server = server
        self.name = str(name)

        if data:
            seata = data
        else:
            data = self.server.p.getqueue(self.name)[self.name]

        self.state_count = data['state_count']
        self.total_jobs = data['total_jobs']
#        self.mtime = data['mtime']
        self.max_walltime = data.get('resources_max.walltime', None)
        self.default_walltime = data.get('resources_default.walltime', None)
        self.type = data['queue_type']
        self.priority = data.get('Priority', None)
        self.enabled = data['enabled']
        self.nodes = data.get('resources_assigned.nodect', None)
        self.started = data['started']

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

        if data:
            data = data
        else:
            data = self.server.p.getnode(self.name)[self.name]

        self.type = data['ntype']
        self.np = int(data['np'])

        if 'jobs' in data:
            self.np_used = len(data['jobs'].split(','))
        else:
            self.np_used = 0

        if data['state'] == 'free' and 'jobs' in data:
            self.state = 'partial'
        else:
            self.state = data['state']
        self.jobs = data.get('jobs', None)
        self.job_list = self.get_job_list()

    def __str__(self):
        return self.name

    def _get_pk_val(self):
        return self.name

    def is_free(self):
        if self.state == 'free':
            return True
        return False

    def is_online(self):
        state = self.state
        if len(state.split(',')) > 1 or state == 'down' or state == 'offline':
            return False
        return True
    
    def get_job_list(self):

        job_list = RelationList()

        try:
            jobs = self.jobs.split(',')
        except:
            jobs = []

        for j in jobs:

            full_id = j[j.index('/')+1:]
            id, host = full_id.split('.', 1)
            job_list.append(Job(server=self.server, id=id, full_id=full_id))
                

        return job_list

    def get_absolute_url(self):
        return '/servers/%s/nodes/%s/' % (self.server, self.name)
        


class RelationList(list):
    
    pass

        
