# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_bouncy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bounce',
            name='diagnostic_code',
            field=models.TextField(max_length=5000, null=True, blank=True),
        ),
    ]
