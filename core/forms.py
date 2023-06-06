from django import forms
from .models import User, Habit

class AddHabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'type', 'hours', 'done_today']
        labels = {'name': 'Habit Name', 'type': 'Once per day habit, or a hours per day'}
        #if (Habit.done_today == True):
            #widgets = {'hours': forms.HiddenInput()}
            
        