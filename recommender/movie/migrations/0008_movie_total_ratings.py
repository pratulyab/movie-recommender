# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-16 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_movie_mean_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='total_ratings',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
