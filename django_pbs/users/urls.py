from django.conf.urls.defaults import *

urlpatterns = patterns('django_pbs.users.views',

                    
    (r'^(?P<username>[-.\w]+)/$', 'user_detail'),
)
