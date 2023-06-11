from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Habit, Tracker
from django.contrib.auth.decorators import login_required
from .forms import AddHabitForm, AddTrackerForm, addObserverForm, AddCommentForm
from datetime import date, timedelta, datetime
from django.http import JsonResponse
from django.db.models.functions import ExtractYear, ExtractMonth
from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette


alert = None
def authenticate(request, owner):
    if (request.user == owner):
        return True
    else:
        return False

def no_permission(request):
    return render(request, 'core/no_permission.html')
#----------------------------------------------MAIN PAGE VIEWS---------------------------------------------
# Create your views here.
@login_required
def index(request):
    pk = None
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

    if alert is not None:
        pk = alert[0]
    
    
    context = {
        'user': request.user,
        'habit': habits,
        "observers": observing,
        "dict": observer_dict,
        "names": observer_names,
        "pk":pk,
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
        habit_form = form.save(commit=False)
        habit_form.user = request.user
        habit_form.save()
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
    req = request.user.id
    if req == habit.user_id:
        habit.delete()
        return redirect('home')
    else:
        return redirect('no_permission')

@login_required
def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    req = request.user.id
    if req == habit.user_id:
        if (request.method == 'GET'):
            form = AddHabitForm(instance = habit) 
        else:
            form = AddHabitForm(request.POST, instance = habit)
            if form.is_valid():
                form.save()
                return redirect('habit_detail', habit.pk)
        return render(request, 'core/edit_habit.html', {'form': form})
    else:
        return redirect('no_permission')

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
    habit = get_object_or_404(Habit, pk=pk)
    req = request.user.id
    if req == habit.user_id:
        user_list = User.objects.all()
        if (request.method == 'GET'):
            form = addObserverForm(instance = habit) 
        else:
            form = addObserverForm(request.POST, instance = habit)
            if form.is_valid():
                form.save()
                return redirect('habit_detail', habit.pk)
        return render(request, 'core/add_observer.html', {'form': form, 'user_list': user_list})
    else:
        return redirect('no_permission')


def delete_observer(request, pk):
    pass



#----------------------------------------------HABIT DETAILS---------------------------------------------
def get_missing_trackers(trackers):
    first_day = trackers[0].date_completed
    second_day = trackers[1].date_completed
    d = first_day - second_day
    tracker_days = []

    if d.days > 1:
        for i in range(d.days + 1):
            tracker_days.append(first_day + timedelta(days=i - d.days))
    else:
        return None

    tracker_days.pop(0)
    tracker_days.pop(len(tracker_days) - 1)
    #list(reversed(tracker_days))
    return tracker_days


def habit_detail(request, pk):


#-----------authenitcation
    current_user = request.user.id
    current_user_name = request.user
    habit = get_object_or_404(Habit, pk=pk)
    observers = habit.observers
    if habit.user_id == current_user or request.user.username == observers:

#-----Misc variables
        trackers = Tracker.objects.filter(habit_id = habit).order_by("-date_completed")
        completed_time = 0
        owner = habit.user_id
        type = habit.type
        recent_missing_tracker_days = get_missing_trackers(trackers)


#-------variables for chart data
        habit_chart_data = []
        habit_raw_date_data = []
        habit_date_data = []
        organized = []
        i = 0

        for tracker in trackers:
            completed_time += tracker.goal_status
            habit_raw_date_data.append(tracker.date_completed)
            actual_date = tracker.date_completed.strftime('%m-%d-%Y')
            habit_date_data.append(actual_date)
            habit_chart_data.append(tracker.goal_status)

        while i < len(habit_chart_data) - 1:
            organized.append({'t': habit_raw_date_data[i], 'y': habit_chart_data[i]})
            i += 1

#---data for dynamic weekday add, and best day to add 
        current_date = date.today()
        last_week = current_date - timedelta(days=6)
        best = best_day(habit_raw_date_data)

#---------Comment section
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

#-----------------dump for chart
        data = {
            "dates": habit_date_data,
            "nums": habit_chart_data
        }

        context = {
            'habit': habit, 
            "trackers": trackers,
            "current_date": current_date,
            "last_week": last_week,
            "completed_time": completed_time,
            "type": type,
            "best_day": best,
            "current_user": current_user,
            "current_username": current_user_name,
            "observers": observers,
            'owner': owner,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            "request": the_requeset,
            "missing": recent_missing_tracker_days,
            "data": data,
            "hab": habit_date_data,
            'organized': organized,
            }
        return render(request, 'core/habit_detail.html', context)
    else:
        return redirect("no_permission")

def tracker_chart(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    trackers = Tracker.objects.filter(habit_id = habit).order_by("date_completed")
    first_day = trackers[0].date_completed
    last_day = trackers[len(trackers) - 1].date_completed
    d = last_day - first_day
    tracker_days = []
    tracker_data = {}
    for i in range(d.days + 1):
        tracker_days.append(first_day + timedelta(days=i))
        tracker_data[(first_day + timedelta(days=i)).strftime('%Y,%m,%d')] = 0

    for tracker in trackers:
        tracker_data[(tracker.date_completed).strftime('%Y,%m,%d')] = tracker.goal_status

    return JsonResponse({
        "title": 'Habit Hours per Day',
        "data": {
            "labels": {
                "tracker_days": tracker_days,
                "tracker_data": tracker_data
            },
            "datasets": [{
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": tracker_data
            }]
        }
    })




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
    req = request.user.id
    if req == habit.user_id:
        if request.method == "GET":
            form = AddTrackerForm()
        else:
            form = AddTrackerForm(request.POST)
            if form.is_valid():
                tracker = form.save(commit = False)
                tracker.user_id = request.user.id
                tracker.habit_id = pk
                tracker.save()
                return redirect('habit_detail', pk)
        return render(request, 'core/add_tracker.html', {"form": form})

    else:
        return redirect('no_permission')



def edit_tracker(request, pk):
    tracker = get_object_or_404(Tracker, pk=pk)
    habit = Habit.objects.get(pk = pk)
    req = request.user.id
    if req == habit.user_id:
        if (request.method == 'GET'):
            form = AddTrackerForm(instance = tracker) 
        else:
            form = AddTrackerForm(request.POST, instance = tracker)
            if form.is_valid():
                form.save()
                return redirect('tracker_detail')
        return render(request, 'core/edit_tracker.html', {'form': form, "tracker": tracker})
    else:
        return redirect('no_permission')



def delete_tracker(request, pk):
    habit = Habit.objects.get(pk = pk)
    req = request.user.id
    if req == habit.user_id:
        tracker = Tracker.objects.get(pk = pk)
        tracker.delete()
        return redirect('home')

    else:
        return redirect('no_permission')


#----------------------------------------------COMMENT VIEWS---------------------------------------------
