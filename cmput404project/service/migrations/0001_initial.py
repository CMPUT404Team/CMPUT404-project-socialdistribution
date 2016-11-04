# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 23:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=30)),
                ('displayName', models.CharField(max_length=30)),
                ('friends', models.ManyToManyField(blank=True, to='service.Author')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('pubDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('comment', models.CharField(max_length=200)),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('published', models.DateTimeField(verbose_name=b'date published')),
                ('visibility', models.CharField(choices=[(b'PU', b'PUBLIC'), (b'PR', b'PRIVATE'), (b'FR', b'FRIENDS'), (b'FO', b'FOAF'), (b'SO', b'SERVERONLY')], default=b'PUBLIC', max_length=10)),
                ('title', models.CharField(blank=True, default=b'Title', max_length=75)),
                ('source', models.CharField(blank=True, editable=False, max_length=100)),
                ('origin', models.CharField(blank=True, editable=False, max_length=100)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('contentType', models.CharField(default=b'text/plain', editable=False, max_length=100)),
                ('categories', models.CharField(blank=True, max_length=200)),
                ('next', models.CharField(blank=True, editable=False, max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Post'),
        ),
        migrations.AddField(
            model_name='category',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Post'),
        ),
    ]
