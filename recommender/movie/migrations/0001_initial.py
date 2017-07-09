# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-09 14:06
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('year', models.CharField(blank=True, max_length=4)),
                ('imdbID', models.CharField(max_length=10, unique=True)),
                ('tmdbID', models.CharField(max_length=10, unique=True)),
                ('movielensID', models.PositiveIntegerField(unique=True)),
                ('mean_rating', models.DecimalField(decimal_places=7, default=Decimal('0'), max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('5'))], verbose_name='Average Rating')),
                ('visits', models.PositiveIntegerField(default=0)),
                ('outbounds', models.TextField(blank=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
                ('genres', models.ManyToManyField(related_name='movies', to='movie.Genre')),
            ],
        ),
    ]
