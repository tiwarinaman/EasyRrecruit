from django import template

from jobportal.models import Job, Recruiter

register = template.Library()


@register.simple_tag(name='is_same_recruiter')
def is_job_already_applied(job, user):
    recu = Recruiter.objects.get(uname=user)
    same = Job.objects.filter(id=job, recruiter=recu)

    if same:
        return True
    else:
        return False