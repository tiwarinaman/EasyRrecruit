from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Candidate Model

class Candidate(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    candidate_number = models.BigIntegerField(null=True)
    dob = models.DateField(null=True)
    candidate_image = models.FileField(upload_to='candidate_profile/', null=True)
    gender = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.uname.first_name + " " + self.uname.last_name


# Recruiter Model

class Recruiter(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recruiter_number = models.BigIntegerField(null=True)
    company_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    recruiter_image = models.FileField(upload_to='recruiter_profile/', null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.uname.first_name + " " + self.uname.last_name


# Admin Model

class Admin(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    admin_number = models.BigIntegerField(null=True)
    dob = models.DateField(null=True)
    admin_image = models.FileField(upload_to='admin_profile/', null=True)
    gender = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.uname.first_name + " " + self.uname.last_name


# Post Job Model

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=100, null=True)
    job_location = models.CharField(max_length=100, null=True)
    job_type = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    salary = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    last_date = models.DateField(null=True)
    skills = models.CharField(max_length=200, null=True)
    website_link = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True, null=True)
    company_logo_image = models.FileField(upload_to='post_job_company_logo/', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title + " By " + self.recruiter.company_name + " - " + self.recruiter.uname.first_name


class ApplyJob(models.Model):
    job_applied = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=True)
    resume = models.FileField(upload_to='candidate_resume/', null=True)

    def __str__(self):
        return self.candidate.uname.username + " " + self.job_applied.job_title


class BookmarkJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.user.first_name + " - " + self.job.job_title


class Query(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=250)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(blank=True, null=True)
    is_replied = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject} || Is Replied - {self.is_replied}"


class QueryReply(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query.name} - {self.query.subject}"
