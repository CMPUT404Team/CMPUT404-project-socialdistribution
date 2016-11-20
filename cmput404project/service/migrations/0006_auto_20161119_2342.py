# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_auto_20161119_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='host',
        ),
        migrations.RemoveField(
            model_name='node',
            name='port',
        ),
        migrations.AddField(
            model_name='node',
            name='baseUrl',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='password',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='username',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
