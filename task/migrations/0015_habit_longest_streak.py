# Generated by Django 2.1.4 on 2019-01-13 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0014_auto_20190109_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='longest_streak',
            field=models.IntegerField(default=0),
        ),
    ]