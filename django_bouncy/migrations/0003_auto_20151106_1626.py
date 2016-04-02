# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_bouncy', '0002_auto_20150927_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
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
                ('feedback_id', models.CharField(max_length=100, null=True, blank=True)),
                ('feedback_timestamp', models.DateTimeField(null=True, verbose_name=b'Feedback Time', blank=True)),
                ('delivered_time', models.DateTimeField(null=True, blank=True)),
                ('processing_time', models.PositiveSmallIntegerField(default=0)),
                ('smtp_response', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'deliveries'
            },
        ),
        migrations.AlterField(
            model_name='bounce',
            name='feedback_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bounce',
            name='feedback_timestamp',
            field=models.DateTimeField(null=True, verbose_name=b'Feedback Time', blank=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='feedback_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='feedback_timestamp',
            field=models.DateTimeField(null=True, verbose_name=b'Feedback Time', blank=True),
        ),
    ]
