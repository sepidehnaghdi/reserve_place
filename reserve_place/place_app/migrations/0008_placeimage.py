# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('place_app', '0007_rentercomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image_file')),
                ('description', models.TextField(blank=True, null=True)),
                ('image_name', models.CharField(blank=True, max_length=255)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='place_app.Place')),
            ],
        ),
    ]