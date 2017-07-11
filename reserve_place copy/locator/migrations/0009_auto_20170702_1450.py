# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 14:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0008_auto_20170627_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locatorprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]