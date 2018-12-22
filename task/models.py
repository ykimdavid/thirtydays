from django.db import models
from django.utils import timezone

# Create your models here.
class Habit(models.Model):
    habit_name = models.CharField(max_length=200)
    start_date = models.DateTimeField('date published')
    habit_desc = models.TextField()
    habit_priority = models.IntegerField()

    def __str__(self):
        return self.habit_name

    def days_left(self):
        elapsed = timezone.now() - self.start_date
        days_left = 30 - elapsed.days
        return days_left
