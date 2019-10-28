# Generated by Django 2.2.5 on 2019-10-26 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExceptionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, verbose_name='Url')),
                ('traceback', models.TextField(verbose_name='Traceback')),
                ('msg', models.CharField(max_length=255, verbose_name='msg')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]