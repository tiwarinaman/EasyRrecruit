# Generated by Django 3.1.4 on 2021-01-17 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0007_candidate_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiter',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]
