# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_auto_20161102_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, default=b'Title', max_length=75),
        ),
    ]
