from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", blank=True, null=True)
    image_url = models.CharField(max_length=64, blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings")
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="listings_won")

    def __str__(self):
        return f"{self.title} for ${self.current_price}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.current_price = self.starting_price
        super().save(*args, **kwargs)
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")  
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")  
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"${self.amount} by {self.user.username} on {self.listing.title}"
    
class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name='watchers')
    
    def __str__(self):
        return f"{self.username}"
     
