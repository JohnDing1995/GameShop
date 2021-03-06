# Generated by Django 2.1.3 on 2019-01-10 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='game_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='pid',
            field=models.TextField(default=-1, primary_key=True, serialize=False),
        ),
    ]
