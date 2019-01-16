from django.db import models
from django.forms import ModelForm, SelectDateWidget, MultipleChoiceField, CheckboxSelectMultiple
from django.utils import timezone
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
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

    DAYSOFWEEK = [
        (0, 'Monday'),
        (1, 'Tuesdsay'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateField(default=datetime.date.today) #TODO: add validation against future dates
    current_streak = models.IntegerField(default = 0)
    longest_streak = models.IntegerField(default = 0)
    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=NORMAL)
    completed = models.BooleanField(default = False)
    active = models.BooleanField(default = True)
    last_update = models.DateField(null=True)
    tracked_days = MultiSelectField(choices=DAYSOFWEEK)
    #quit

    def __str__(self):
        return self.name

    # assume ran once a day w celery
    def update(self):
        today = datetime.date.today()
        self.active = str(today.weekday()) in self.tracked_days

        if self.active:
            self.updateEvent()

            if today > self.last_update: #next day resetting
                if self.completed:
                    self.completed = False
                else:
                    self.current_streak = 0
                    self.start_date = today


        self.last_update = today
        self.save()

    def updateEvent(self): # creates event for day if doesn't exist, updates ow.
        today = datetime.date.today()
        event = Event.objects.filter(date=today).first()

        if not event:
            event = Event.objects.create(
                user=self.user,
                date=today,
                status='None',
            )
            event.save()
            event.initializeEvent()
            event.update()
        else:
            event.update()
            event.save()

    def complete(self):
        if self.active:
            if not self.completed:
                self.completed = True
                self.current_streak += 1

                if (self.current_streak > self.longest_streak):
                    self.longest_streak = self.current_streak

                self.save()

    def initializeHabit(self):
        today = datetime.datetime.now().date()
        #if self.start_date > today:
        #    self.active = False

        #if self.start_date < today:
        #    elapsed = today - self.start_date
        #    self.current_streak = elapsed.days
        #    self.longest_streak = elapsed.days

        self.last_update = today
        self.save()


class Event(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habits = models.ManyToManyField(Habit)
    date = models.DateField()
    status = models.CharField(max_length=10)
    note = models.TextField(blank=True)

    def __str__(self):
        name = self.date.strftime('%m-%d-%Y') + f': {self.status}'
        return name

    def initializeEvent(self): # updates event habits for day
        today = datetime.date.today()
        active_habits = Habit.objects.filter(user=self.user, active=True)
        for habit in active_habits:
            self.habits.add(habit)
        self.save()

    def update(self):
        self.initializeEvent()
        total = self.habits.count() #total number of active habits for day
        completed = 0 # completed counter
        for habit in self.habits.all():
            if habit.completed:
                completed += 1

        if completed == 0:
            self.status='None'
        elif completed == total:
            self.status='Perfect'
        else:
            self.status='Partial'

        self.save()



class AddForm(ModelForm):
    tracked_days = MultipleChoiceField(choices=Habit.DAYSOFWEEK)
    tracked_days.initial = ['0', '1', '2', '3', '4', '5', '6']
    class Meta:
        model = Habit
        exclude = ('current_streak', 'completed', 'active', 'user', 'last_update', 'longest_streak', 'start_date')
        widgets = {
            'start_date': SelectDateWidget(years=range(datetime.date.today().year - 5, datetime.date.today().year + 1)),
        }
    def save(self, commit=True):
        tracked_days = self.cleaned_data['tracked_days']
        habit = super(AddForm, self).save(commit=False)

        if commit:
            habit.tracked_days = tracked_days
            habit.save()
        return habit
