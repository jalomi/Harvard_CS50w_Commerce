from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="account")

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description =  models.CharField(max_length=200)
    starting_bid = models.IntegerField()
    img_url = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} starting at {self.starting_bid} by {self.user}"

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass