from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    created_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.__name__
    
class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=True) #True = completed
    
    class Meta:
        unique_together = ('habit', 'date')
        
    def __str__(self):
        return f'{self.habit.name} - {self.date}'