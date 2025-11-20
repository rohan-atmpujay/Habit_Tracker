from django.contrib import admin
from .models import Habit, HabitRecord

# Register your models here.
admin.site.register(Habit)
admin.site.register(HabitRecord)