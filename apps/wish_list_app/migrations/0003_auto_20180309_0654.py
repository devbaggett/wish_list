# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-09 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_list_app', '0002_auto_20180309_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
