# Generated by Django 2.1.3 on 2019-01-25 12:29

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20190118_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='time',
            field=models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='time',
            field=models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now),
        ),
    ]
