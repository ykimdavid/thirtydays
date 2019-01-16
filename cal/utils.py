from datetime import datetime, timedelta
from calendar import HTMLCalendar
from task.models import Event

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
    def formatday(self, day, events):
        event = events.filter(date__day=day).first()
        if day != 0:
            if event:
                if event.status == 'Perfect':
                    return f"<td style='background-color:#a5d6a7;'><span class='date'>{day}</span></td>"
                elif event.status == 'Partial':
                    return f"<td style='background-color:#f0f4c3;'><span class='date'>{day}</span></td>"
                elif event.status == 'None':
                    return f"<td style='background-color:#ffcdd2;'><span class='date'>{day}</span></td>"
            else:
                return f"<td ><span class='date'>{day}</span></td>"
        return '<td></td>'

	# formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
    def formatmonth(self, user, withyear=True):
        events = Event.objects.filter(user=user)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
