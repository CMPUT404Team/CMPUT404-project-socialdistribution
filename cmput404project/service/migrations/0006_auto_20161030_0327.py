# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_auto_20161030_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='friends',
            field=models.ManyToManyField(blank=True, to='service.Author'),
        ),
    ]