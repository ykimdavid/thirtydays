# Generated by Django 2.1.4 on 2019-01-05 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20190105_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='habit',
            name='day_counter',
            field=models.IntegerField(default=0),
        ),
    ]
