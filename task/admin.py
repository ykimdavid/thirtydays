from django.contrib import admin
from .models import Habit, Event

# Register your models here.
admin.site.register(Habit)
admin.site.register(Event)
