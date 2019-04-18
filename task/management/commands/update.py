from django.core.management.base import BaseCommand, CommandError
from task.models import Habit, Event
from django.contrib.auth.models import User
import schedule, time, datetime


class Command(BaseCommand):
    help = "runs update function"

    def update():
        today = datetime.date.today()
        users = User.objects.all()
        for habit in Habit.objects.all():
            habit.update()

        for user in users:
            event = Event.objects.create(
                user=user,
                date=today,
                status='None',
                )
            event.initializeEvent()
            event.save()



    def handle(self, *args, **options):
        schedule.every().day.at("00:00").do(self.update)
        while True:
            schedule.run_pending()
            time.sleep(60)
