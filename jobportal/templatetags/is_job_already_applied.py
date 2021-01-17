from django import template

from jobportal.models import ApplyJob

register = template.Library()


@register.simple_tag(name='is_job_already_applied')
def is_job_already_applied(job, user):
    applied = ApplyJob.objects.filter(job_applied_id=job, candidate__uname=user)
    if applied:
        return True
    else:
        return False
