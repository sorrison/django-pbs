from django.template import Library
from django.conf import settings

register = Library()


@register.inclusion_tag('pbs_jobs/job_table_base.html')
def job_table(job_list, type):

    running = False
    if type == 'Running':      
        running = True   

    return {'job_list': job_list, 'running': running, 'MEDIA_URL': settings.MEDIA_URL }
