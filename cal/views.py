from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required
from django.views import generic
from .utils import Calendar
from task.models import Event

# Create your views here.

@login_required
def monthView(request):
    d = datetime.date.today()
    user = request.user
    e = Event.objects.get(date = d, user=user)
    e.updateStatus()
    e.save()
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(user=user, withyear=True)
    html_cal = html_cal.replace('<td ', '<td width="150" height="100" ')

    context = {
        'calendar': html_cal,
    }



    return render(request, 'cal/monthView.html', context)
