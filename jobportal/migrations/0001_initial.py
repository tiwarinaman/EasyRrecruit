# Generated by Django 3.1.4 on 2021-01-12 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recruiter_number', models.BigIntegerField(null=True)),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('recruiter_image', models.FileField(null=True, upload_to='recruiter_profile/')),
                ('status', models.CharField(max_length=100, null=True)),
                ('uname', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_number', models.BigIntegerField(null=True)),
                ('candidate_image', models.FileField(null=True, upload_to='candidate_profile/')),
                ('gender', models.CharField(max_length=100, null=True)),
                ('uname', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
