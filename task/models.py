from django.db import models
from django.forms import ModelForm, SelectDateWidget, DateField
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Habit(models.Model):
    LOW = 0
    NORMAL = 1
    HIGH = 2

    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=200, unique=True)
    start_date = models.DateField(default=datetime.date.today)
    day_counter = models.IntegerField(default = 0)
    habit_desc = models.TextField(blank=True)
    habit_priority = models.IntegerField(choices=PRIORITY_CHOICES, default=NORMAL)
    completed = models.BooleanField(default = False)
    active = models.BooleanField(default = True)
    last_update = models.DateField(null=True)

    def __str__(self):
        return self.habit_name

    def update(self):
        today = datetime.datetime.now().date()
        if self.active:
            if today > self.last_update:
                if self.completed:
                    self.completed = False
                else:
                    self.day_counter = 0
                    self.start_date = today
        else:
            if self.start_date <= today:
                self.active = True

        self.last_update = today
        self.save()

    def complete(self):
        if not self.completed:
            self.completed = True
            self.day_counter += 1
            self.save()

    def initializeHabit(self):
        today = datetime.datetime.now().date()
        if self.start_date > today:
            self.active = False

        if self.start_date < today:
            elapsed = today - self.start_date
            self.day_counter = elapsed.days

        self.last_update = today
        self.save()



class AddForm(ModelForm):
    class Meta:
        model = Habit
        exclude = ('day_counter', 'completed', 'active', 'user', 'last_update')
        widgets = {
            'start_date': SelectDateWidget(years=range(datetime.date.today().year - 10, datetime.date.today().year + 10))
        }
