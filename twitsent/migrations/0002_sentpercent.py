# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitsent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentPercent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=30)),
                ('sent_perc', models.CharField(max_length=50)),
            ],
        ),
    ]
