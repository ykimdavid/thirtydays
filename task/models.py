from django.db import models
from django.forms import ModelForm, ChoiceField, Select
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Habit(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    PRIORITY_CHOICES = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=200)
    start_date = models.DateField()
    day_counter = models.IntegerField(default = 0)
    habit_desc = models.TextField()
    habit_priority = models.IntegerField()
    completed = models.BooleanField(default = False)
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.habit_name


    def update(self):
        now = datetime.datetime.now()
        if self.active:
            current_date = self.start_date + datetime.timedelta(days = self.day_counter)
            midnight = datetime.datetime(current_date.year, current_date.month, current_date.day + 1, 0, 0, 0)

            if  now > midnight:
                if self.completed == False:
                    self.day_counter = 0
                    self.start_date = current_date
                else:
                    self.day_counter += 1
                    self.completed = False

        else:
            if self.start_date <= now.date():
                self.active = True

        self.save()


    def initializeHabit(self):
        today = datetime.datetime.now().date()
        if self.start_date > today:
            self.active = False

        if self.start_date < today:
            elapsed = today - self.start_date
            self.day_counter = elapsed.days

        self.save()



class AddForm(ModelForm):
    class Meta:
        model = Habit
        exclude = ('day_counter', 'completed', 'active', 'user')
