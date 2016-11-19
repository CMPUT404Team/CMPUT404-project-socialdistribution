# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20161030_0121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='friends',
        ),
        migrations.AddField(
            model_name='author',
            name='friends',
            field=models.ManyToManyField(to='service.Author'),
        ),
    ]