from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Habit
from .models import AddForm
from django.template import RequestContext

# Create your views here.
def index(request):
    if request.method == 'POST':
        complete = request.POST.get('complete')
        delete = request.POST.get('delete')

        if complete:
            print(complete)
            habit = get_object_or_404(Habit, pk = complete)
            print(habit.completed)
            habit.completed = True
            print(habit.completed)
            habit.save()

        if delete:
            print(delete)
            habit = get_object_or_404(Habit, pk = delete)
            habit.delete()


    habit_list = Habit.objects.all()
    for habit in habit_list:
        habit.update()

    context = {'habit_list': habit_list}
    return render(request, 'task/index.html', context)

def detail(request, id):
    for habit in Habit.objects.all():
        habit.update()

    habit = get_object_or_404(Habit, pk = id)
    context = {'habit': habit}
    return render(request, 'task/detail.html', context)

def addHabit(request):
    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            newHabit = form.save()
            newHabit.initializeHabit()

            print(newHabit.day_counter)

            return HttpResponseRedirect('/task/')

    else:
        form = AddForm()

    return render(request, 'task/addHabit.html', {'form': form})
