from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Habit
from .forms import AddHabitForm

# Create your views here.
def index(request):
    user = get_object_or_404(User)
    habit = Habit.objects.all()
    context = {
        'user': user,
        'habit': habit
    }
    return render(request, 'core/index.html', context)

def add_habit(request):
    if request.method == 'POST':
        form = AddHabitForm(request.POST)
        habit = form.save(commit=False)
        habit.save()
        return redirect('home')
    else:
        form = AddHabitForm()
    
    return render(request, 'core/add_habit.html', {'form': form})


def delete_habit(request, pk):
    habit = Habit.objects.get(pk = pk)
    habit.delete()
    return redirect('home')


def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if (request.method == 'GET'):
        form = AddHabitForm(instance = habit) 
    else:
        form = AddHabitForm(request.POST, instance = habit)
        if form.is_valid():
            form.save()
            return redirect('habit_detail', habit.pk)
    return render(request, 'core/edit_habit.html', {'form': form})


def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    return render(request, 'core/habit_detail.html', {'habit': habit})