from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
import markdown

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

