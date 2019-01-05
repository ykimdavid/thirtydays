from django.test import TestCase
from task.models import Habit
import datetime


def create_habit(name="testHabit", days=0, desc="description", priority=1, completed=False):
    """ Create a habit with 'days' number of days offset from now. Set days as
    a negative integer for habits created in the past, positive for future """
    date = datetime.datetime.now().date() + datetime.timedelta(days = days)

    habit = Habit.objects.create(
        habit_name = name,
        start_date = date,
        habit_desc = desc,
        habit_priority = priority,
        completed = completed
    )

    habit.initializeOldHabit()

    return habit



class HabitTests(TestCase):
    def testDayCounter(self):
        """ Tests efficacy of initializeOldHabit method"""
        today = datetime.datetime.now().date()
        habit = create_habit(
            "testHabit1",
            -10,
            "testHabit1 description",
            1,
            False
        )

        self.assertIs(habit.day_counter == 10, True)
        current_date = habit.start_date + datetime.timedelta(days = habit.day_counter)
        self.assertIs(current_date == today, True)

    def testActive_update_completed(self):
        """ Tests else case of active method """
        habit = create_habit(completed = True)
        today = datetime.datetime.now().date()
        self.assertIs(habit.start_date == today, True)
        self.assertIs(habit.day_counter == 0, True)
        self.assertIs(habit.completed, True)

        """By changing start_date and calling active, we modify current_date to
        yesterday midnight. Since the habit was completed, calling active should
        increment the day_counter and set completed to False."""

        habit.start_date -= datetime.timedelta(days = 2)
        habit.active()

        self.assertIs(habit.day_counter, 1)
        self.assertIs(habit.completed, False)


    def testActive_update_notcompleted(self):
        """ Tests non-completed case of active method """
        today = datetime.datetime.now().date()
        habit = create_habit(days = -10)
        self.assertIs(habit.day_counter, 10)

        """By changing start_date and calling active, we modify current_date to
        yesterday midnight. Since the habit was not, calling active should reset
        the day_counter to 0 and set start_date to the current_date."""

        habit.start_date -= datetime.timedelta(days = 2)
        habit.active()

        current_date = today - datetime.timedelta(days = 2)
        self.assertIs(habit.day_counter, 0)
        self.assertIs(habit.start_date == current_date, True)


    def testActive_noUpdate(self):
        """ Tests that habit attributes do not update when now <= midnight """
        habit = create_habit()
        habit.active()
        today = datetime.datetime.now().date()
        self.assertIs(habit.day_counter, 0)
        self.assertIs(habit.start_date == today, True)
        self.assertIs(habit.completed, False)



# Create your tests here.
