from django.test import TestCase
from task.models import Habit
import datetime


class HabitTestCase(TestCase):
    def setUp(self):
        Habit.objects.create(
        habit_name = "TestHabit1",
        start = datetime.datetime.now().date(),
        habit_desc = "Description",
        habit_priority = 1
        )

        Habit.objects.create(
        habit_name = "TestHabit2",
        start = datetime.datetime.now().date() - datetime.timedelta(days = 10),
        habit_desc = "Description2",
        habit_priority = 2
        )


    def test_habit_completion(self):
        habit1 = Habit.objects.get(habit_name = "TestHabit1")
        habit2 = Habit.objects.get(habit_name = "TestHabit2")

        habit1.active()
        habit2.active()


# Create your tests here.
