# Generated by Django 2.1.5 on 2019-01-13 05:34

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0015_habit_longest_streak'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='trackedDays',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(3, 'Thursday'), (0, 'Monday'), (2, 'Wednesday'), (4, 'Friday'), (5, 'Saturday'), (1, 'Tuesdsay'), (6, 'Sunday')], max_length=13, null=True),
        ),
    ]