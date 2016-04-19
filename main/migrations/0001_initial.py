# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers
import main.models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=500)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date and Time')),
                ('house_points', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='FAQEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('category', models.CharField(max_length=25, choices=[(b"Regents' Scholarship", b"Regents' Scholarship"), (b'Academic', b'Academic'), (b'Social', b'Social')])),
            ],
        ),
        migrations.CreateModel(
            name='HousePointsOther',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('points_R', models.IntegerField()),
                ('points_C', models.IntegerField()),
                ('points_S', models.IntegerField()),
                ('points_A', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name=b'Date and Time')),
            ],
        ),
        migrations.CreateModel(
            name='ScholarContactProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('majors', models.CharField(max_length=200)),
                ('minors', models.CharField(max_length=200, blank=True)),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(10000)])),
                ('interests_extracurriculars', models.TextField()),
                ('blurb', models.TextField()),
                ('picture', models.ImageField(null=True, upload_to=main.models.PlacePicture(b'img/scholar_contacts'), blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='ScholarContactProfileView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=40)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('scholar_contact_profile', models.ForeignKey(to='main.ScholarContactProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('sid', models.IntegerField()),
                ('house', models.CharField(max_length=1, choices=[(b'R', b'Rockefeller'), (b'C', b'Chavez'), (b'S', b'Savio'), (b'A', b'Apperson'), (b'N', b'Not Applicable')])),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(to='main.Student'),
        ),
    ]
