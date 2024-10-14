from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")
def heidi(request):
    return HttpResponse("Hello, Heidi")
def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!"),
def goodbye(request, name): 
    return render(request, "hello/goodbye.html", {
        "name": name.capitalize()
    })
