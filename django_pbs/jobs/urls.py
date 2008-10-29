from django.conf.urls.defaults import *

urlpatterns = patterns('django_pbs.jobs.views',

                    
    (r'^(?P<job_id>[-.\w]+)/$', 'job_detail'),
)
