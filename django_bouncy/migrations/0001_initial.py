# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bounce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('sns_topic', models.CharField(max_length=350)),
                ('sns_messageid', models.CharField(max_length=100)),
                ('mail_timestamp', models.DateTimeField()),
                ('mail_id', models.CharField(max_length=100)),
                ('mail_from', models.EmailField(max_length=254)),
                ('address', models.EmailField(max_length=254)),
                ('feedback_id', models.CharField(max_length=100)),
                ('feedback_timestamp', models.DateTimeField(verbose_name=b'Feedback Time')),
                ('hard', models.BooleanField(db_index=True, verbose_name=b'Hard Bounce')),
                ('bounce_type', models.CharField(max_length=50, verbose_name=b'Bounce Type', db_index=True)),
                ('bounce_subtype', models.CharField(max_length=50, verbose_name=b'Bounce Subtype', db_index=True)),
                ('reporting_mta', models.TextField(null=True, blank=True)),
                ('action', models.CharField(db_index=True, max_length=150, null=True, verbose_name=b'Action', blank=True)),
                ('status', models.CharField(db_index=True, max_length=150, null=True, blank=True)),
                ('diagnostic_code', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('sns_topic', models.CharField(max_length=350)),
                ('sns_messageid', models.CharField(max_length=100)),
                ('mail_timestamp', models.DateTimeField()),
                ('mail_id', models.CharField(max_length=100)),
                ('mail_from', models.EmailField(max_length=254)),
                ('address', models.EmailField(max_length=254)),
                ('feedback_id', models.CharField(max_length=100)),
                ('feedback_timestamp', models.DateTimeField(verbose_name=b'Feedback Time')),
                ('useragent', models.TextField(null=True, blank=True)),
                ('feedback_type', models.CharField(db_index=True, max_length=150, null=True, verbose_name=b'Complaint Type', blank=True)),
                ('arrival_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
