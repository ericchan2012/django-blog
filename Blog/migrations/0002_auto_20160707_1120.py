# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-07 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='navigation',
            field=models.CharField(choices=[('0', '\u65b0\u95fb'), ('1', '\u6559\u7a0b'), ('2', '\u8d44\u6e90')], default='0', max_length=1, verbose_name='\u5bfc\u822a\u540d\u5b57'),
        ),
    ]
