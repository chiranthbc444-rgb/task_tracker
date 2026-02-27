from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'completed', 'due_date', 'created_at')
    list_filter = ('priority', 'status', 'completed')
    search_fields = ('title', 'description')
    list_editable = ('completed',)
