# Generated by Django 3.1.7 on 2021-03-31 10:14

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0016_auto_20210331_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='education',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='qualification',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
