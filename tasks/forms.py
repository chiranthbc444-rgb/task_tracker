from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter task title…',
                'autofocus': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Add a description (optional)…',
                'rows': 4,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-input form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-input form-select',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
        }
