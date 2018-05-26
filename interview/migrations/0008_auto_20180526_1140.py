# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-05-26 09:40
from __future__ import unicode_literals

from django.db import migrations


def migrate_state(apps, schema_editor):
    Interview = apps.get_model('interview', 'Interview')
    Process = apps.get_model('interview', 'Process')
    for i in Interview.objects.all():
        i.save()

    for p in Process.objects.all():
        p.save()

    for p in Process.objects.filter(state='OP'):
        if p.interview_set.exists():
            p.state = 'WK'
        else:
            p.state = 'WP'

class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0007_auto_20180526_0944'),
    ]

    operations = [
        migrations.RunPython(migrate_state),
    ]
