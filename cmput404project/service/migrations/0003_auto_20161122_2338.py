# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 23:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_node_nodemanager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='port',
        ),
        migrations.AddField(
            model_name='node',
            name='path',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
