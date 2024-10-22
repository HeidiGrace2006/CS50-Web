from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search, name='search'),
    path('create/', views.create, name="create"),
    path('edit/', views.edit, name="edit"),
    path('save_edit/', views.save_edit, name="save_edit"),
    path("wiki/<str:entry>/", views.entry, name="entry"),
    path("random/", views.random_page, name="random"),
]
