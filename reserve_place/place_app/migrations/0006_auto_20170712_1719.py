# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 17:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('place_app', '0005_auto_20170712_1715'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Renting',
            new_name='Rent',
        ),
    ]
