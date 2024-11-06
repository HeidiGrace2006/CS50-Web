from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'starting_price', 'description', 'category', 'image_url']
        labels = {
            'title': 'Listing Title',
            'starting_price': 'Starting Price',
            'description': 'Description',
            'category': 'Category',
            'image_url': 'Image URL',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        }
        
def create(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('listing', listing_id=listing.id)
    form = CreateListing()
    return render(request, "auctions/create.html", {
        "form": form
    })

@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)
    
    return redirect('listing', listing_id=listing_id)

class BidForm(forms.Form):
    bid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Enter your bid'}),
    )

    def __init__(self, *args, **kwargs):
        self.current_price = kwargs.pop('current_price', 0)
        self.starting_price = kwargs.pop('starting_price', 0)
        super().__init__(*args, **kwargs)
        self.fields['bid'].validators.append(self.validate_bid)

    def validate_bid(self, bid):
        if bid <= self.current_price and self.current_price > self.starting_price:
            raise forms.ValidationError("Bid must be higher than the current price.")
        elif bid < self.starting_price:
            raise forms.ValidationError("Bid must be at least the starting bid.")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add a comment...', 'rows': 3}),
        }

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    on_watchlist = listing in request.user.watchlist.all()

    # Get the user's last bid for this listing
    users_bid = listing.bids.filter(user=request.user).order_by('-id').first()
    highest_bid = listing.bids.order_by('-amount').first()
    highest_bidder = users_bid and users_bid.amount == listing.current_price

    form = BidForm(request.POST or None, current_price=listing.current_price, starting_price=listing.starting_price)
    comment_form = CommentForm(request.POST or None)

    if request.method == "POST":
        if 'close_listing' in request.POST:
            listing.is_closed = True
            listing.winner = highest_bid.user
            listing.save()
        elif form.is_valid():
            bid_amount = form.cleaned_data["bid"]
            bid = Bid.objects.create(listing=listing, user=request.user, amount=bid_amount)
            bid.save()

            listing.current_price = bid_amount
            listing.save()

            return redirect('listing', listing_id=listing_id)
        elif comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
            return redirect('listing', listing_id=listing_id)
        
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "on_watchlist": on_watchlist,
        "form": form,
        "comment_form": comment_form,
        "highest_bidder": highest_bidder,
        "comments": listing.comments.order_by('-timestamp'),
    })
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(category_id=category_id)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

