# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 17:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0005_auto_20170627_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locatorprofile',
            name='created_at',
        ),
    ]