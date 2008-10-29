from django.conf.urls.defaults import *

urlpatterns = patterns('django_pbs.moab.views',


    #url(r'^$', 'moab_index', name='pbs_moab_index'),                     
    url(r'^showstart/$', 'showstart', name='pbs_showstart'),
)



