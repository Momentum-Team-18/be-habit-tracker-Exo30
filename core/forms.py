from django import forms
from .models import User, Habit, Tracker
from django.utils import timezone

class AddHabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'type', 'hours', 'done_today']
        labels = {'name': 'Habit Name', 'type': 'Once per day habit, or a hours per day'}
        #if (Habit.done_today == True):
            #widgets = {'hours': forms.HiddenInput()}
            

class AddTrackerForm(forms.ModelForm):
    date_completed = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=('Year', 'Month', 'Day')
        ), initial=timezone.now(),
    )

    class Meta: 
        model = Tracker
        fields = ("date_completed", "goal_status")
        labels = {"goal_status": "Hours/Times completed"}