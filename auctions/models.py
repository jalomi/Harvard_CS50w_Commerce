from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="account")
    wins = models.ManyToManyField('Listing', blank=True, related_name="auction_wins")

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    value = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.CharField(max_length=200)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)

class Listing(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description =  models.CharField(max_length=200)
    starting_bid = models.IntegerField()
    img_url = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} starting at {self.starting_bid} by {self.user}"
