# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 15:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RenterProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(max_length=15)),
                ('image_of_national_card', models.FileField(upload_to='')),
                ('image_of_birth_certificate', models.FileField(upload_to='')),
                ('birth_certificate_number', models.IntegerField()),
                ('national_number', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
