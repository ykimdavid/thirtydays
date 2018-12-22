from django.shortcuts import render, get_object_or_404
from .models import Habit
# Create your views here.
def index(request):
    habit_list = Habit.objects.order_by('habit_priority')[:5]
    context = {'habit_list': habit_list}
    return render(request, 'task/index.html', context)

def detail(request, id):
    habit = get_object_or_404(Habit, pk = id)
    context = {'habit': habit}
    return render(request, 'task/detail.html', context)
