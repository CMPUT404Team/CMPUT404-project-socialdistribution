# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-26 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20161126_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='contentType',
            field=models.CharField(default=b'text/plain', editable=False, max_length=100),
        ),
    ]