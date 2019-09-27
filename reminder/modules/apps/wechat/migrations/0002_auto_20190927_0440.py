# Generated by Django 2.2.5 on 2019-09-27 04:40

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechat',
            name='funcscope_categories',
            field=models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='权限集'),
        ),
    ]
