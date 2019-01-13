# Generated by Django 2.1.4 on 2019-01-05 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='completed',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='habit',
            name='current_streak',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='habit',
            name='start_date',
            field=models.DateField(),
        ),
    ]
