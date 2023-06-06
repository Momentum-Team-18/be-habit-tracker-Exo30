from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    birthdate = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username



class Habit(models.Model):
    HOURS = 'HR'
    DAYS = "TD"
    TYPE_CHOICES = [
        (HOURS, 'Hours a day'),
        (DAYS, 'Times a day'),
    ]
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=DAYS,)
    hours = models.IntegerField(default=0)
    done_today = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.name
    
