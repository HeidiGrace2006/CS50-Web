from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name="index"),
    path ("heidi", views.heidi, name="heidi"),
    #path ("<str:name>", views.greet, name="greet"),
    path ("<str:name>", views.goodbye, name="goodbye")
]