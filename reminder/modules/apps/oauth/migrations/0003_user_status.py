# Generated by Django 2.2.5 on 2019-10-28 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0002_auto_20191008_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('InActive', 'InActive')], default='Active', max_length=32, verbose_name='Status'),
        ),
    ]
