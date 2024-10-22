from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from . import util
import markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    if request.method == "POST":
        query = request.POST.get("q")

        entry_content =  util.get_entry(query) 
        if entry_content:
            return redirect(reverse("entry", kwargs={"entry": query}))
        else:
            entries = util.list_entries()
            results = [entry for entry in entries if query.lower() in entry.lower()] # append an entry to the list 'results' if query is a substring of an entry

            return render(request, "encyclopedia/results.html", {
                "query": query,
                "results": results
            })
    return redirect(reverse("index"))   

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
            "message": f"Entry with title '{title}' already exists."
        })
        
        else:
            #save the page as a md file (Title.md) in the folder entries
            util.save_entry(title, content)
            return redirect(reverse("entry", kwargs={"entry": title}))
    return render(request, "encyclopedia/create.html")
 
class EditForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(
        label='Content',
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 40})
    )

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        form = EditForm(initial={
            "title": title,
            "content": content
        })

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form" : form,
        })

def save_edit(request):
    return

def entry(request, entry):
    entry_content = util.get_entry(entry)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"No entry found for '{entry}'. "
        })

    entry_content = markdown.markdown(entry_content)

    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": entry_content
    })

def random_page(request):
    entries = util.list_entries()

    random_page = random.choice(entries)

    return redirect(reverse("entry", kwargs={"entry": random_page}))
