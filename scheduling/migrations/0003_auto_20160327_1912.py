# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 23:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('scheduling', '0002_class_document_instructor_schedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='version',
            new_name='name',
        ),
    ]
