from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Candidate, Recruiter, Job, ApplyJob, BookmarkJob

# Register Your Site Here

admin.site.site_header = "Easy-Recruit Admin Dashboard"
admin.site.unregister(Group)
admin.site.register(Candidate)
admin.site.register(Recruiter)

admin.site.register(Job)
admin.site.register(ApplyJob)
admin.site.register(BookmarkJob)