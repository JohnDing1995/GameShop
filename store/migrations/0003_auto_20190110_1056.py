# Generated by Django 2.1.3 on 2019-01-10 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20190110_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='id',
        ),
        migrations.AlterField(
            model_name='game',
            name='game_name',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='pid',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
