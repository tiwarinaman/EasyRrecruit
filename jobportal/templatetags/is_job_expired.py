from django import template
import datetime
from jobportal.models import Job

register = template.Library()


@register.simple_tag(name='is_job_expired')
def is_job_expired(job):
    expired = Job.objects.get(id=job)
    today = datetime.datetime.today()
    t = datetime.datetime(today.year, today.month, today.day)
    l = datetime.datetime.strptime(str(expired.last_date), "%Y-%m-%d")

    if l < t:
        return True
    else:
        return False


