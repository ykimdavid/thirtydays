from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Habit
from .models import AddForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    current_user = request.user
    if request.method == 'POST':
        complete = request.POST.get('complete')
        delete = request.POST.get('delete')

        if complete:
            habit = get_object_or_404(Habit, pk = complete)
            habit.complete()

        if delete:
            habit = get_object_or_404(Habit, pk = delete)
            habit.delete()

    habit_list = Habit.objects.filter(user=current_user).order_by('-habit_priority')

    for habit in habit_list:
        habit.update()

    is_empty = False
    if not habit_list:
        is_empty = True

    incomplete = habit_list.filter(completed=False)
    complete = habit_list.filter(completed=True)
    context = {
        'complete_habit': complete,
        'incomplete_habit': incomplete,
        'is_empty': is_empty,
    }
    return render(request, 'task/index.html', context)

@login_required(login_url='/login/')
def detail(request, id):
    for habit in Habit.objects.all():
        habit.update()

    habit = get_object_or_404(Habit, pk = id)
    context = {'habit': habit}
    return render(request, 'task/detail.html', context)

@login_required(login_url='/login/')
def addHabit(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            newHabit = form.save(commit=False)
            newHabit.user = current_user
            newHabit.initializeHabit()

            return HttpResponseRedirect('/task/')

    else:
        form = AddForm()

    return render(request, 'task/addHabit.html', {'form': form})

@login_required(login_url='/login/')
def editHabit(request, id):
    habit = get_object_or_404(Habit, pk = id)
    form = AddForm(request.POST or None, instance=habit)
    if form.is_valid():
        form.save()
        habit.initializeHabit()
        return HttpResponseRedirect('/task/')

    return render(request, 'task/editHabit.html', {'form': form, 'id':habit.id})

@login_required(login_url='/login/')
def user_settings(request):
    return render(request, 'task/settings.html')
