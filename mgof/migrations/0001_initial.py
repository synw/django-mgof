# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='Edited')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Published'), (1, 'Pending'), (2, 'Unpublished')])),
                ('num_topics', models.IntegerField(default=0, verbose_name='Topics in forum')),
                ('num_posts', models.IntegerField(default=0, verbose_name='Posts in forum')),
                ('last_post_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('last_post_username', models.CharField(max_length=120, editable=False, blank=True)),
                ('is_public', models.BooleanField(default=True, verbose_name='Public')),
                ('authorized_groups', models.ManyToManyField(to='auth.Group', verbose_name='Reserved to groups', blank=True)),
                ('editor', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Edited by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='Edited')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(null=True, verbose_name='Content', blank=True)),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Published'), (1, 'Pending'), (2, 'Unpublished')])),
                ('responded_to_pk', models.PositiveIntegerField(default=0, blank=True)),
                ('responded_to_username', models.CharField(default=b'', max_length=120, blank=True)),
                ('editor', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Edited by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('posted_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Posted by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Post',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='Edited')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Published'), (1, 'Pending'), (2, 'Unpublished')])),
                ('num_posts', models.IntegerField(default=0, verbose_name='Number of posts')),
                ('num_views', models.IntegerField(default=0, verbose_name='Number of views')),
                ('last_post_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('last_post_username', models.CharField(max_length=120, editable=False, blank=True)),
                ('is_closed', models.BooleanField(default=False, verbose_name='Topic closed')),
                ('is_moderated', models.BooleanField(default=True, verbose_name='Topic is moderated')),
                ('editor', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Edited by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('forum', models.ForeignKey(related_name='topics', verbose_name='Forum', to='mgof.Forum')),
                ('posted_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Posted by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(related_name='posts', verbose_name='Topic', to='mgof.Topic'),
        ),
    ]
