# Generated by Django 2.1.5 on 2019-01-09 21:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_auto_20190108_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]