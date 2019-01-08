from django.test import TestCase
from task.models import Habit
from django.urls import reverse
from django.contrib.auth.models import User
from freezegun import freeze_time

import datetime

USER_PASSWORD = "testing321"

def create_habit(user, name="testHabit", days=0, desc="description", priority=1, completed=False):
    """ Create a habit with 'days' number of days offset from now. Set days as
    a negative integer for habits created in the past, positive for future """
    date = datetime.datetime.now().date() + datetime.timedelta(days = days)

    habit = Habit.objects.create(
        user = user,
        habit_name = name,
        start_date = date,
        habit_desc = desc,
        habit_priority = priority,
        completed = completed
    )

    habit.initializeHabit()

    return habit

class TestUtil(TestCase):
    def testFreezeTime(self):
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        self.assertEqual(datetime.datetime.now(), datetime.datetime(2012, 1, 14, 12, 0, 1))
        freezer.stop()

class HabitTests(TestCase):
    def testDayCounter(self):
        """ Tests efficacy of initializeHabit method"""
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        today = datetime.datetime.now().date()
        habit = create_habit(user=user, days = -10)

        self.assertIs(habit.day_counter, 10)
        current_date = habit.start_date + datetime.timedelta(days = habit.day_counter)
        self.assertEqual(current_date, today)


    def testUpdate_update_completed(self):
        """ Tests else case of update method """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        habit = create_habit(user=user)
        today = datetime.datetime.now().date()
        habit.complete()
        self.assertEqual(habit.start_date, today)
        self.assertIs(habit.day_counter, 1)
        self.assertIs(habit.completed, True)

        tomorrow = today + datetime.timedelta(days = 1)
        with freeze_time(tomorrow):
            habit.update()
            self.assertIs(habit.day_counter, 1)
            self.assertIs(habit.completed, False)


    def testUpdate_update_notcompleted(self):
        """ Tests non-completed case of update method """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        habit = create_habit(user=user, days = -10)
        today = datetime.datetime.now().date()

        self.assertIs(habit.day_counter, 10)

        tomorrow = today + datetime.timedelta(days = 1)
        with freeze_time(tomorrow):
            habit.update()
            self.assertIs(habit.day_counter, 0)
            self.assertEqual(habit.start_date, tomorrow)


    def testUpdate_noUpdate(self):
        """ Tests that habit attributes do not update during the same day. """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        habit = create_habit(user=user)
        habit.update()
        today = datetime.datetime.now().date()
        self.assertIs(habit.day_counter, 0)
        self.assertEqual(habit.start_date, today)
        self.assertIs(habit.completed, False)

    def testFutureHabit(self):
        """ Tests efficacy of future habits and active tag. """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        habit = create_habit(user=user, days = 10)
        today = datetime.datetime.now().date()
        futuredate = datetime.datetime.now().date() + datetime.timedelta(days = 10)

        self.assertIs(habit.day_counter, 0)
        self.assertEqual(habit.start_date, futuredate)
        self.assertIs(habit.active, False)

        not_quite_futuredate = today + datetime.timedelta(days = 5)
        with freeze_time(not_quite_futuredate):
            habit.update()
            self.assertIs(habit.day_counter, 0)
            self.assertEqual(habit.start_date, futuredate)
            self.assertIs(habit.active, False)

    def testUpdate_futureHabit(self):
        """ Tests if active tag is updated when a future habit reaches start day. """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        habit = create_habit(user=user, days = 10)
        self.assertIs(habit.active, False)
        
        futuredate = habit.start_date + datetime.timedelta(days = 10)
        with freeze_time(futuredate):
            habit.update()
            self.assertIs(habit.active, True)


class HabitIndexViewTests(TestCase):
    def test_no_habits(self):
        response = self.client.get(reverse('Habits'))
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, [])
        self.assertQuerysetEqual(incompleted, [])

    def test_incomplete_habits(self):
        habit1 = create_habit(name='habit1')
        habit2 = create_habit(name='habit2')
        habit3 = create_habit(name='habit3')

        response = self.client.get(reverse('Habits'))
        self.assertEqual(response.status_code, 200)

        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, [])
        self.assertQuerysetEqual(incompleted, ['<Habit: habit1>', '<Habit: habit2>', '<Habit: habit3>'])

    def test_complete_habits(self):
        habit1 = create_habit(name='habit1', completed=True)
        habit2 = create_habit(name='habit2', completed=True)
        habit3 = create_habit(name='habit3')

        response = self.client.get(reverse('Habits'))
        self.assertEqual(response.status_code, 200)

        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>'])
        self.assertQuerysetEqual(incompleted, ['<Habit: habit3>'])

    def test_completion(self):
        habit1 = create_habit(name='habit1', completed=True)
        habit2 = create_habit(name='habit2', completed=True)
        habit3 = create_habit(name='habit3')

        response = self.client.get(reverse('Habits'))
        self.assertEqual(response.status_code, 200)

        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>'])
        self.assertQuerysetEqual(incompleted, ['<Habit: habit3>'])


        response = self.client.post(reverse('Habits'), {'complete': habit3.id})
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']
        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>', '<Habit: habit3>'])
        self.assertQuerysetEqual(incompleted, [])

    def test_deletion(self):
        habit1 = create_habit(name='habit1', completed=True)
        habit2 = create_habit(name='habit2', completed=True)
        habit3 = create_habit(name='habit3')
        response = self.client.get(reverse('Habits'))
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>'])

        response = self.client.post(reverse('Habits'), {'delete': habit1.id})
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        self.assertQuerysetEqual(completed, ['<Habit: habit2>'])

    # def check_user_auth(self):
    #     self.user = create_user('testuser')
    #     login = self.client.login('testuser', USER_PASSWORD)
    #     response = self.client.get(reverse('Habits'))
    #
    #

#TODO Test the order of habits by priority
#TODO Test detail view
#TODO Test addHabit Form
#TODO Test editHabit Form
