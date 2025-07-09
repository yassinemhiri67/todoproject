"""Admin configuration for the todo app."""

from django.contrib import admin

from .models import Employee, Snippet, Task

admin.site.register(Employee)  # Register Employee model
admin.site.register(Task)      # Register Task model
admin.site.register(Snippet)   # Register Snippet model

# Register your models here.
