from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Habit, Tracker
from django.contrib.auth.decorators import login_required
from .forms import AddHabitForm, AddTrackerForm

# Create your views here.
@login_required
def index(request):
    habit = Habit.objects.filter(user=request.user).order_by('name')
    context = {
        'user': request.user,
        'habit': habit
    }
    return render(request, 'core/index.html', context)

def account_detail(request):
    user = request.user
    return render(request, 'core/account_detail.html', {"user": user})

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = AddHabitForm(data=request.POST)
        habit = form.save(commit=False)
        habit.user = request.user
        habit.save()
        return redirect('home')
    else:
        form = AddHabitForm()
        trackerForm = AddTrackerForm()
    context = {
        "form": form
    }
    
    return render(request, 'core/add_habit.html', context)

@login_required
def delete_habit(request, pk):
    habit = Habit.objects.get(pk = pk)
    habit.delete()
    return redirect('home')

@login_required
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
    trackers = Tracker.objects.all()
    habit = get_object_or_404(Habit, pk=pk)
    return render(request, 'core/habit_detail.html', {'habit': habit, "trackers": trackers})

def list_tracker(request):
    trackers = Tracker.objects.all()
    return render(request, 'core/habit_detail.html', {'trackers': trackers})

def tracker_detail(request, pk):
    tracker = get_object_or_404(Tracker, pk=pk)
    context = {
        "tracker": tracker,
        "entry_date": tracker.date_completed,
        "result": tracker.goal_status
    }
    return render(request, 'core/tracker_detail.html', context)

def add_tracker(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == "GET":
        form = AddTrackerForm()
    else:
        form = AddTrackerForm(request.POST)
        if form.is_valid():
            tracker = form.save(commit = False)
            tracker.user = request.user
            tracker.habit_id = pk
            tracker.save()
            return redirect('habit_detail', pk)


    return render(request, 'core/add_tracker.html', {"form": form})



def edit_tracker(request, pk):
    tracker = get_object_or_404(Tracker, pk=pk)
    if (request.method == 'GET'):
        form = AddTrackerForm(instance = tracker) 
    else:
        form = AddTrackerForm(request.POST, instance = tracker)
        if form.is_valid():
            form.save()
            return redirect('tracker_detail')
    return render(request, 'core/edit_tracker.html', {'form': form, "tracker": tracker})


def delete_tracker(request, pk):
    tracker = Tracker.objects.get(pk = pk)
    tracker.delete()
    return redirect('home')