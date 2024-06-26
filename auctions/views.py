from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing

class NewListingForm(forms.Form):
    title = forms.CharField(label="",
                            widget=forms.TextInput(attrs={"placeholder":"Title"}))
    description = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={"placeholder":"Description"}))
    starting_bid = forms.IntegerField(label="",
                                      widget=forms.NumberInput(attrs={"placeholder":"Starting Bid"}))
    img_url = forms.CharField(label="",
                              required=False,
                              widget=forms.TextInput(attrs={"placeholder":"Image URL (Optional)"}))
    category = forms.CharField(label="",
                               required=False,
                               widget=forms.TextInput(attrs={"placeholder":"Category (Optional)"}))


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
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
    

def new_listing(request):
    
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            img_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]

            listing = Listing(user=user,
                              title=title,
                              description=description,
                              starting_bid=starting_bid,
                              img_url=img_url,
                              category=category)
            
            listing.save()

            # redirect to new listing
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        else:
            return render(request, "auctions/add.html", {
                "error": "ERROR: Invalid input"
            })
    else:
        return render(request, "auctions/add.html", {
            "form": NewListingForm(),
        })
    
def listing(request, id):
    listing = Listing.objects.get(pk=id)
    in_watchlist = listing in User.objects.get(username=request.user).watchlist.all()
    return render(request, "auctions/listing.html", {
        "id": listing.id,
        "title": listing.title,
        "description": listing.description,
        "user": listing.user,
        "in_watchlist": in_watchlist,

    })

def watchlist(request):
    user = User.objects.get(username=request.user)
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "listings": user.watchlist.all(),
    })

def watch(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["id"])
        user = User.objects.get(username=request.user)
        user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("index"))
    
def unwatch(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["id"])
        user = User.objects.get(username=request.user)
        user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("index"))
