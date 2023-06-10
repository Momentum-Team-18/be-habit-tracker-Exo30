from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.constraints import UniqueConstraint

# Create your models here.


class User(AbstractUser):
    birthdate = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username



class Habit(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    HOURS = 'HR'
    DAYS = "Day"
    habit_choices = [
        ("Good", "Starting A Good Habit"),
        ("Bad", "Ending A Bad Habit"),
    ]
    TYPE_CHOICES = [
        (HOURS, 'Hours a day'),
        (DAYS, 'Times a day'),
    ]
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=DAYS,)
    hours = models.IntegerField(default=0)
    target = models.IntegerField(default=False)
    done_today = models.BooleanField(null=True, default=False)
    good_or_bad = models.CharField(max_length=50, choices=habit_choices, default="Good")
    observers = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.name
    
class Tracker(models.Model):
    habit = models.ForeignKey(to=Habit, on_delete=models.CASCADE, null= True)
    date_completed = models.DateField()
    goal_status = models.IntegerField(null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["habit", "date_completed"], name="habit_date")
        ]
    
    #def percentage(self):
        #return int((self / self.habit.target) * 100)
    
    def __str__(self):
        return self.habit
    
    def goal_num(self):
        result = 0
        result += int(self.date_completed)
        return result
    

class Comment(models.Model):
    habit = models.ForeignKey(Habit,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)