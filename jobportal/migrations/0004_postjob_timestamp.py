# Generated by Django 3.1.4 on 2021-01-16 12:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0003_postjob_website_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='postjob',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]