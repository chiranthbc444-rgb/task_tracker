import os
import sys
from django.conf import settings

# ----------------------------
# DJANGO SETTINGS (Single File)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY='secret-key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': False,
            'OPTIONS': {
                'loaders': [
                    ('django.template.loaders.locmem.Loader', {
                        'index.html': """
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Task Tracker</title>
                            <style>
                                body { font-family: Arial; margin: 40px; }
                                .completed { text-decoration: line-through; color: gray; }
                            </style>
                        </head>
                        <body>
                        <h1>Task Tracker</h1>
                        <form method="post">
                            {% csrf_token %}
                            <input type="text" name="title" placeholder="New Task" required>
                            <button type="submit">Add</button>
                        </form>
                        <ul>
                            {% for task in tasks %}
                                <li class="{% if task.completed %}completed{% endif %}">
                                    {{ task.title }}
                                    {% if not task.completed %}
                                        <a href="/complete/{{ forloop.counter0 }}/">Complete</a>
                                    {% endif %}
                                    <a href="/delete/{{ forloop.counter0 }}/">Delete</a>
                                </li>
                            {% endfor %}
                        </ul>
                        </body>
                        </html>
                        """
                    }),
                ],
            },
        },
    ],
)

import django
django.setup()

from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from django.core.management import execute_from_command_line

# ----------------------------
# SIMPLE MODEL
# ----------------------------
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    class Meta:
        app_label = 'tasks'

# Create table manually
from django.db import connection
with connection.schema_editor() as schema_editor:
    try:
        schema_editor.create_model(Task)
    except:
        pass

# ----------------------------
# VIEWS
# ----------------------------
def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(title=title)
        return redirect("/")
    tasks = Task.objects.all()
    return render(request, "index.html", {"tasks": tasks})

def complete(request, id):
    tasks = list(Task.objects.all())
    if id < len(tasks):
        task = tasks[id]
        task.completed = True
        task.save()
    return redirect("/")

def delete(request, id):
    tasks = list(Task.objects.all())
    if id < len(tasks):
        tasks[id].delete()
    return redirect("/")

# ----------------------------
# URLS
# ----------------------------
urlpatterns = [
    path('', index),
    path('complete/<int:id>/', complete),
    path('delete/<int:id>/', delete),
]

# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == "__main__":
    execute_from_command_line([sys.argv[0], "runserver"])