from django.conf.urls.defaults import *

urlpatterns = patterns('django_pbs.servers.views',


    url(r'^$', 'server_list', name='pbs_server_list'),                     
    url(r'^(?P<server_id>[-.\w]+)/$', 'server_detail', name='pbs_server_detail'),
    url(r'^(?P<server_id>[-.\w]+)/queues/$', 'queue_list', name='pbs_queue_list'),
    url(r'^(?P<server_id>[-.\w]+)/queues/(?P<queue_id>[-.\w]+)/$', 'queue_detail', name='pbs_queue_detail'),
    url(r'^(?P<server_id>[-.\w]+)/nodes/$', 'node_list', name='pbs_node_list'),
    #(r'^(?P<server_id>[-.\w]+)/nodes/(?P<node_id>[-.\w]+)/$', 'node_detail'),
)


urlpatterns += patterns('django_pbs.jobs.views',

    url(r'^jobs/(?P<job_id>[-.\w]+)/$', 'job_detail', name='pbs_job_detail'),
)

urlpatterns += patterns('django_pbs.users.views',

    url(r'^users/(?P<username>[-.\w]+)/$', 'user_detail', name='pbs_user_detail'),
)
