# Generated by Django 2.1.3 on 2019-02-15 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_game_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='category',
            field=models.CharField(default='No category', max_length=256),
        ),
    ]
