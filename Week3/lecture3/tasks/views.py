from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

# Create your views here.
def index(request):
    if "tasks" not in request.session: #aka, if user on that session doesn't have a task list yet
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST) #request.POST contains data that the user submits
        if form.is_valid():  # Check if form data is valid (server-side)
            task = form.cleaned_data["task"]  # Isolate the task from the 'cleaned' version of form data
            task.append(task)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })