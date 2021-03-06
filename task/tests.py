from django.test import TestCase
from task.models import Habit, Event
from task.management.commands.update import Command
from django.urls import reverse
from django.contrib.auth.models import User
from freezegun import freeze_time
from django.db.utils import IntegrityError
from django.db import transaction, IntegrityError
import datetime


def create_habit(user, name="testHabit", days=0, desc="description", priority=1, completed=False, tracked_days=['0', '1', '2', '3', '4', '5', '6'], longest_streak=0, current_streak=0):
    """ Create a habit with 'days' number of days offset from now. Set days as
    a negative integer for habits created in the past, positive for future """
    date = datetime.datetime.now().date() + datetime.timedelta(days = days)

    habit = Habit.objects.create(
        user = user,
        name = name,
        start_date = date,
        description = desc,
        priority = priority,
        completed = completed,
        tracked_days=tracked_days,
        longest_streak=longest_streak,
        current_streak=current_streak,
    )

    habit.initializeHabit()
    if completed:
        habit.complete()

    return habit

class TestUtil(TestCase):
    def testFreezeTime(self):
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        self.assertEqual(datetime.datetime.now(), datetime.datetime(2012, 1, 14, 12, 0, 1))
        freezer.stop()

class HabitTests(TestCase): #TODO: test longest_streak
    #NOTE: OUTDATED
    # def testDayCounter(self):
    #     """ Tests efficacy of initializeHabit method of previous habit"""
    #     user = User.objects.create_user(username='testuser', password='12345')
    #     login = self.client.login(username='testuser', password='12345')
    #     today = datetime.datetime.now().date()
    #     habit = create_habit(user=user, days = -10)
    #
    #     self.assertIs(habit.current_streak, 10)
    #     current_date = habit.start_date + datetime.timedelta(days = habit.current_streak)
    #     self.assertEqual(current_date, today)


    def testUpdate_update_completed(self):
        """ Tests else case of update method """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit = create_habit(user=user)
        today = datetime.datetime.now().date()
        habit.complete()
        self.assertEqual(habit.start_date, today)
        self.assertIs(habit.current_streak, 1)
        self.assertTrue(habit.completed)

        tomorrow = today + datetime.timedelta(days = 1)
        with freeze_time(tomorrow):
            Command.update()
            habit.update()
            self.assertIs(habit.current_streak, 1)
            self.assertFalse(habit.completed)


    def testUpdate_update_notcompleted(self):
        """ Tests non-completed case of update method """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit = create_habit(user=user)
        today = datetime.datetime.now().date()
        self.assertIs(habit.current_streak, 0)

        tomorrow = today + datetime.timedelta(days = 1)
        with freeze_time(tomorrow):
            Command.update()
            habit.update()
            self.assertIs(habit.current_streak, 0)
            self.assertEqual(habit.start_date, tomorrow)


    def testUpdate_noUpdate(self):
        """ Tests that habit attributes do not update during the same day. """
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit = create_habit(user=user)
        habit.update()
        today = datetime.datetime.now().date()
        self.assertIs(habit.current_streak, 0)
        self.assertEqual(habit.start_date, today)
        self.assertIs(habit.completed, False)

#NOTE: OUTDATED
    # def testFutureHabit(self):
    #     """ Tests efficacy of future habits and active tag. """
    #     user = User.objects.create_user(username='testuser', password='12345')
    #     login = self.client.login(username='testuser', password='12345')
    #     habit = create_habit(user=user, days = 10)
    #     today = datetime.datetime.now().date()
    #     futuredate = datetime.datetime.now().date() + datetime.timedelta(days = 10)
    #
    #     self.assertIs(habit.current_streak, 0)
    #     self.assertEqual(habit.start_date, futuredate)
    #     self.assertIs(habit.active, False)
    #
    #     not_quite_futuredate = today + datetime.timedelta(days = 5)
    #     with freeze_time(not_quite_futuredate):
    #         habit.update()
    #         self.assertIs(habit.current_streak, 0)
    #         self.assertEqual(habit.start_date, futuredate)
    #         self.assertIs(habit.active, False)

#NOTE: OUTDATED
    # def testUpdate_futureHabit(self):
    #     """ Tests if active tag is updated when a future habit reaches start day. """
    #     user = User.objects.create_user(username='testuser', password='12345')
    #     login = self.client.login(username='testuser', password='12345')
    #     habit = create_habit(user=user, days = 10)
    #     self.assertIs(habit.active, False)
    #
    #     futuredate = habit.start_date + datetime.timedelta(days = 10)
    #     with freeze_time(futuredate):
    #         habit.update()
    #         self.assertTrue(habit.active)

    def testDuplicateHabit(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit = create_habit(user=user)
        with transaction.atomic():
            self.assertRaises(IntegrityError, lambda: create_habit(user=user))

    def testLongestStreak(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit = create_habit(user=user, current_streak=5, longest_streak=7)
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        tomorrowmorrow = today + datetime.timedelta(days=2)
        tomorrowmorrowmorrow = today + datetime.timedelta(days=3)
        self.assertFalse(habit.completed)
        habit.complete()
        habit.update()
        self.assertTrue(habit.completed)
        self.assertIs(habit.current_streak, 6)
        self.assertIs(habit.longest_streak, 7)

        with freeze_time(tomorrow):
            Command.update()
            habit.update()
            habit.complete()
            habit.update()
            self.assertTrue(habit.completed)
            self.assertIs(habit.current_streak, 7)
            self.assertIs(habit.longest_streak, 7)

        with freeze_time(tomorrowmorrow): #increment longest streak
            Command.update()
            habit.update()
            habit.complete()
            habit.update()
            self.assertTrue(habit.completed)
            self.assertIs(habit.current_streak, 8)
            self.assertIs(habit.longest_streak, 8)

        with freeze_time(tomorrowmorrowmorrow):
            Command.update()
            habit.update()
            self.assertFalse(habit.completed)
            self.assertIs(habit.current_streak, 8)
            self.assertIs(habit.longest_streak, 8)

        with freeze_time(tomorrowmorrowmorrow + datetime.timedelta(days=1)): #current streak resets
            Command.update()
            habit.update()
            self.assertFalse(habit.completed)
            self.assertIs(habit.current_streak, 0)
            self.assertIs(habit.longest_streak, 8)

    def trackedDays1(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit = create_habit(user=user, tracked_days=['0', '1']) #monday and tuesday
        start = datetime.date(2019, 1, 14) #Monday
        with freeze_time(start): #Monday
            Command.update()
            habit.update()
            self.assertTrue(habit.active)
            habit.complete()

        with freeze_time(start + datetime.timedelta(days=1)): #Tuesday
            Command.update()
            habit.update()
            self.assertTrue(habit.active)
            self.assertIs(habit.current_streak, 1)
            habit.complete()
            self.assertIs(habit.current_streak, 2)

        with freeze_time(start + datetime.timedelta(days=2)): #Wednesday
            Command.update()
            habit.update()
            self.assertFalse(habit.active)
            self.assertIs(habit.current_streak, 2)
            habit.complete()
            self.assertIs(habit.current_streak, 2)

        with freeze_time(start + datetime.timedelta(days=3)): #Thursday
            Command.update()
            habit.update()
            self.assertFalse(habit.active)

        with freeze_time(start + datetime.timedelta(days=7)): #Monday
            Command.update()
            habit.update()
            self.assertTrue(habit.active)
            self.assertIs(habit.current_streak, 2)
            habit.complete()
            self.assertIs(habit.current_streak, 3)


class EventTests(TestCase):
    def eventCreation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit1 = create_habit(user=user, name='habit1')
        habit2 = create_habit(user=user, name='habit2')
        habit3 = create_habit(user=user, name='habit3')
        habits = [habit2, habit3]
        habit1.update()
        event = Event.objects.get(date=datetime.date.today())
        self.assertIs(Event.objects.all().count(), 1)
        self.assertIs(event.habits.all().count(), 3)
        self.assertEqual(event.status, 'None')

        habit1.complete()
        habit1.update()
        event = Event.objects.get(date=datetime.date.today())

        self.assertEqual(event.status, 'Partial')
        for habit in habits:
            habit.complete()
            habit.update()
            self.assertTrue(habit.completed)

        event = Event.objects.get(date=datetime.date.today())

        self.assertEqual(event.status, 'Perfect')



class HabitIndexViewTests(TestCase):
    def test_no_habits(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, [])
        self.assertQuerysetEqual(incompleted, [])

    def test_incomplete_habits(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit1 = create_habit(user=user, name='habit1')
        habit2 = create_habit(user=user, name='habit2')
        habit3 = create_habit(user=user, name='habit3')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, [])
        self.assertQuerysetEqual(incompleted, ['<Habit: habit1>', '<Habit: habit2>', '<Habit: habit3>'])

    def test_complete_habits(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit1 = create_habit(user=user, name='habit1', completed=True)
        habit2 = create_habit(user=user, name='habit2', completed=True)
        habit3 = create_habit(user=user, name='habit3')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>'])
        self.assertQuerysetEqual(incompleted, ['<Habit: habit3>'])

    def test_completion(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit1 = create_habit(user=user, name='habit1', completed=True)
        habit2 = create_habit(user=user, name='habit2', completed=True)
        habit3 = create_habit(user=user, name='habit3')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']

        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>'])
        self.assertQuerysetEqual(incompleted, ['<Habit: habit3>'])

        response = self.client.post(reverse('index'), {'complete': habit3.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']
        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>', '<Habit: habit3>'])
        self.assertQuerysetEqual(incompleted, [])

    def test_deletion(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit1 = create_habit(user=user, name='habit1', completed=True)
        habit2 = create_habit(user=user, name='habit2', completed=True)
        habit3 = create_habit(user=user, name='habit3')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        self.assertQuerysetEqual(completed, ['<Habit: habit1>', '<Habit: habit2>'])

        response = self.client.post(reverse('index'), {'delete': habit1.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('index'))
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        self.assertQuerysetEqual(completed, ['<Habit: habit2>'])

    def test_priority_order(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        Command.update()
        habit1 = create_habit(user=user, name='habit1', priority = Habit.LOW)
        habit2 = create_habit(user=user, name='habit2', priority = Habit.NORMAL)
        habit3 = create_habit(user=user, name='habit3', priority = Habit.HIGH)
        habit1c = create_habit(user=user, name='habit1c', priority = Habit.LOW, completed=True)
        habit2c = create_habit(user=user, name='habit2c', priority = Habit.NORMAL, completed=True)
        habit3c = create_habit(user=user, name='habit3c', priority = Habit.HIGH, completed=True)


        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        completed = response.context['complete_habit']
        incompleted = response.context['incomplete_habit']
        self.assertQuerysetEqual(incompleted, ['<Habit: habit3>', '<Habit: habit2>', '<Habit: habit1>'])
        self.assertQuerysetEqual(completed, ['<Habit: habit3c>', '<Habit: habit2c>', '<Habit: habit1c>'])

class HabitDetailViewTests(TestCase):
    def requireLogin(self):
        response = self.client.get(reverse('detail', kwargs={'id':1}))
        self.assertEqual(response.status_code, 302)

    def nonExistentID(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        habit1 = create_habit(user=user, name='habit1')
        id = habit1.id + 1
        self.assertNotEqual(habit.id, id)
        response = self.client.get(reverse('detail', kwargs={'id': id}))
        self.assertEqual(response.status_code, 404)

class HabitAddHabitTests(TestCase):
    def requireLogin(self):
        response = self.client.get(reverse('add_habit'))
        self.assertEqual(response.status_code, 302)

    def testAdd1(self): #NOTE: Failing
        user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        form_input = {
            'name' : 'testHabit1',
            'start_date' : '2019-01-01',
            'description' : 'description',
            'priority' : Habit.LOW,
        }

        response = self.client.post(reverse('add_habit'), form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        habit = Habit.objects.get(name='testHabit1')
        self.assertEqual(habit.name, 'testHabit1')
        sample_date = datetime.date(2019, 1, 1)
        self.assertEqual(habit.description, 'description')
        self.assertEqual(habit.priority, Habit.LOW)
        self.assertEqual(habit.current_streak, 8)
        self.assertEqual(habit.start_date, sample_date)



class HabitEditHabitTests(TestCase):
    def requireLogin(self):
        response = self.client.get(reverse('edit_habit'))
        self.assertEqual(response.status_code, 302)
