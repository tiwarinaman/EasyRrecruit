from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


# Create your models here.


class Candidate(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    candidate_number = models.BigIntegerField(null=True)
    candidate_image = models.FileField(upload_to='candidate_profile/', null=True)
    gender = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.uname.first_name + " " + self.uname.last_name


class Recruiter(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recruiter_number = models.BigIntegerField(null=True)
    company_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    recruiter_image = models.FileField(upload_to='recruiter_profile/', null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.uname.first_name + " " + self.uname.last_name
