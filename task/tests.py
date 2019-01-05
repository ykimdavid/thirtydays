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

    habit.initializeHabit()

    return habit



class HabitTests(TestCase):
    def testDayCounter(self):
        """ Tests efficacy of initializeHabit method"""
        today = datetime.datetime.now().date()
        habit = create_habit(days = -10)

        self.assertIs(habit.day_counter == 10, True)
        current_date = habit.start_date + datetime.timedelta(days = habit.day_counter)
        self.assertIs(current_date == today, True)

    def testUpdate_update_completed(self):
        """ Tests else case of update method """
        habit = create_habit(completed = True)
        today = datetime.datetime.now().date()
        self.assertIs(habit.start_date == today, True)
        self.assertIs(habit.day_counter == 0, True)
        self.assertIs(habit.completed, True)

        """By changing start_date and calling update, we modify current_date to
        yesterday midnight. Since the habit was completed, calling update should
        increment the day_counter and set completed to False."""

        habit.start_date -= datetime.timedelta(days = 2)
        habit.update()

        self.assertIs(habit.day_counter, 1)
        self.assertIs(habit.completed, False)


    def testUpdate_update_notcompleted(self):
        """ Tests non-completed case of update method """
        today = datetime.datetime.now().date()
        habit = create_habit(days = -10)
        self.assertIs(habit.day_counter, 10)

        """By changing start_date and calling update, we modify current_date to
        yesterday midnight. Since the habit was not, calling update should reset
        the day_counter to 0 and set start_date to the current_date."""

        habit.start_date -= datetime.timedelta(days = 2)
        habit.update()

        current_date = today - datetime.timedelta(days = 2)
        self.assertIs(habit.day_counter, 0)
        self.assertIs(habit.start_date == current_date, True)


    def testUpdate_noUpdate(self):
        """ Tests that habit attributes do not update when now <= midnight. """
        habit = create_habit()
        habit.update()
        today = datetime.datetime.now().date()
        self.assertIs(habit.day_counter, 0)
        self.assertIs(habit.start_date == today, True)
        self.assertIs(habit.completed, False)

    def testFutureHabit(self):
        """ Tests efficacy of future habits and active tag. """
        habit = create_habit(days = 10)
        futuredate = datetime.datetime.now().date() + datetime.timedelta(days = 10)

        self.assertIs(habit.day_counter, 0)
        self.assertIs(habit.start_date == futuredate, True)
        self.assertIs(habit.active, False)

    def testUpdate_futureHabit(self):
        """ Tests if active tag is updated when a future habit reaches start day. """
        habit = create_habit(days = 10)
        self.assertIs(habit.active, False)
        habit.start_date -= datetime.timedelta(days = 12)
        habit.update()
        self.assertIs(habit.active, True)


# Create your tests here.
