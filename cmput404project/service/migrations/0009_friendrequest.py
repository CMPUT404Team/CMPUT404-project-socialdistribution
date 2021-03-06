# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20161128_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('displayName', models.CharField(max_length=30)),
                ('requesting_author_id', models.UUIDField(primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Author')),
            ],
        ),
    ]
