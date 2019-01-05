from django.db import models
from django.forms import ModelForm
from django.utils import timezone
import datetime

# Create your models here.
class Habit(models.Model):
    habit_name = models.CharField(max_length=200)
    start_date = models.DateField()
    day_counter = models.IntegerField(default = 0)
    habit_desc = models.TextField()
    habit_priority = models.IntegerField()
    completed = models.BooleanField(default = False)

    def __str__(self):
        return self.habit_name


    def active(self):
        current_date = self.start_date + datetime.timedelta(days = self.day_counter)
        midnight = datetime.datetime(current_date.year, current_date.month, current_date.day + 1, 0, 0, 0)
        now = datetime.datetime.now()

        if  now > midnight:
            print('update')
            if self.completed == False:
                self.day_counter = 0
                self.start_date = current_date
            else:
                self.day_counter += 1
                self.completed = False
        else:
            print('no update')
        self.save()


class AddForm(ModelForm):
    class Meta:
        model = Habit
        fields = ['habit_name', 'start_date', 'habit_desc', 'habit_priority']
