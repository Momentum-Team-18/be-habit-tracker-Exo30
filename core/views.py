from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Habit, Tracker
from django.contrib.auth.decorators import login_required
from .forms import AddHabitForm, AddTrackerForm, addObserverForm, AddCommentForm
from datetime import date, timedelta
import functools


#----------------------------------------------MAIN PAGE VIEWS---------------------------------------------
# Create your views here.
@login_required
def index(request):
    observer_dict = {}
    observer_names= []
    all_habits = Habit.objects.all()
    habits = Habit.objects.filter(user=request.user).order_by('name')
    observing = Habit.objects.filter(observers=request.user).order_by('user')

    for observer in observing:
        if (observer_dict):
            observer_dict[observer.user].append(observer)
        else: 
    
            observer_dict[observer.user] = [observer]
    
    
    context = {
        'user': request.user,
        'habit': habits,
        "observers": observing,
        "dict": observer_dict,
        "names": observer_names
    }
    return render(request, 'core/index.html', context)

def account_detail(request):
    user = request.user
    return render(request, 'core/account_detail.html', {"user": user})


#----------------------------------------------ADD/DELETE/EDIT HABITS---------------------------------------------
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

def best_day(days):
    weekdays = {    
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    weekdaysInt = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
    }
    for day in days:
        day = day.weekday()
        weekdaysInt[day] += 1
    result = max(weekdaysInt, key = weekdaysInt.get)
    return weekdays[result]


#----------------------------------------------OBSERVER VIEWS---------------------------------------------
def add_observer(request, pk):
    user_list = User.objects.all()
    habit = get_object_or_404(Habit, pk=pk)
    if (request.method == 'GET'):
        form = addObserverForm(instance = habit) 
    else:
        form = addObserverForm(request.POST, instance = habit)
        if form.is_valid():
            form.save()
            return redirect('habit_detail', habit.pk)
    return render(request, 'core/add_observer.html', {'form': form, 'user_list': user_list})

def delete_observer(request, pk):
    pass



#----------------------------------------------HABIT DETAILS---------------------------------------------
def habit_detail(request, pk):
    current_user = request.user.id
    habit = get_object_or_404(Habit, pk=pk)
    trackers = Tracker.objects.filter(habit_id = habit).order_by("-date_completed")
    completed_time = 0
    owner = habit.user_id
    type = habit.type
    observers = habit.observers
    days = []

    for tracker in trackers:
        completed_time += tracker.goal_status
        days.append(tracker.date_completed)
    current_date = date.today()
    last_week = current_date - timedelta(days=6)
    best = best_day(days)

    new_comment = None
    comments = habit.comments.filter(active=True)
    the_requeset = request
    initial_data = {
        'name': request.user.username,
        "email": request.user.email,
    }
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST, initial=initial_data)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.habit = habit
            new_comment.save()
    else:
        comment_form = AddCommentForm(initial=initial_data)

 

    context = {
        'habit': habit, 
        "trackers": trackers,
        "current_date": current_date,
        "last_week": last_week,
        "completed_time": completed_time,
        "type": type,
        "best_day": best,
        "current_user": current_user,
        "observers": observers,
        'owner': owner,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        "request": the_requeset,
        }
    return render(request, 'core/habit_detail.html', context)


#----------------------------------------------TRACKER VIEWS---------------------------------------------
def list_tracker(request):
    trackers = Tracker.objects.order_by('date_completed')

    return render(request, 'core/habit_detail.html', {'trackers': trackers})

def tracker_detail(request, pk):
    tracker = get_object_or_404(Tracker, pk=pk)

    context = {
        "tracker": tracker,
        "entry_date": tracker.date_completed,
        "result": tracker.goal_status,
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


#----------------------------------------------COMMENT VIEWS---------------------------------------------
