from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("bid", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>/", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/toggle_watchlist", views.toggle_watchlist, name="toggle_watchlist"),
]

