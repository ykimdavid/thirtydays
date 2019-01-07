from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Habit
from .models import AddForm
from django.template import RequestContext


def index(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        complete = request.POST.get('complete')
        delete = request.POST.get('delete')

        if complete:
            habit = get_object_or_404(Habit, pk = complete)
            habit.completed = True
            habit.save()

        if delete:
            habit = get_object_or_404(Habit, pk = delete)
            habit.delete()

    habit_list = Habit.objects.filter(user=current_user).order_by('habit_priority')

    for habit in habit_list:
        habit.update()

    incomplete = habit_list.filter(completed=False)
    complete = habit_list.filter(completed=True)

    #context = {'habit_list': habit_list}
    context = {
        'complete_habit': complete,
        'incomplete_habit': incomplete,
        'user': current_user,
    }
    return render(request, 'task/index.html', context)

def detail(request, id):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect('login')

    for habit in Habit.objects.all():
        habit.update()

    habit = get_object_or_404(Habit, pk = id)
    context = {'habit': habit}
    return render(request, 'task/detail.html', context)

def addHabit(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect('login')

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

def editHabit(request, id):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect('login')

    habit = get_object_or_404(Habit, pk = id)
    form = AddForm(request.POST or None, instance=habit)
    print(habit.habit_name)
    if form.is_valid():
        form.save()
        habit.initializeHabit()
        return HttpResponseRedirect('/task/')

    return render(request, 'task/editHabit.html', {'form': form, 'id':habit.id})
