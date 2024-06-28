from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Category, Comment

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


class NewCommentForm(forms.Form):
    text = forms.CharField(label="",
                            widget=forms.TextInput(attrs={"placeholder":"Add Comment"}))

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
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            img_url = form.cleaned_data["img_url"]
            category_name = form.cleaned_data["category"]

            category = None
            if category_name:
                category = Category.objects.filter(name=category_name).first()
                if not category:
                    category = Category.objects.create(name=category_name)

            listing = Listing(poster=request.user,
                              title=title,
                              description=description,
                              starting_bid=starting_bid,
                              img_url=img_url,
                              category=category,
                              price=starting_bid)
            
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

    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = listing in User.objects.get(username=request.user).watchlist.all()

    category_name = None
    comments = Comment.objects.filter(listing=listing)

    if listing.category:
        category_name = listing.category.name

    image = listing.img_url

    return render(request, "auctions/listing.html", {
        "id": listing.id,
        "title": listing.title,
        "description": listing.description,
        "poster": listing.poster,
        "user": request.user,
        "in_watchlist": in_watchlist,
        "category": category_name,
        "image": image,
        "comments": comments,
        "form": NewCommentForm(),
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
        User.objects.get(username=request.user).watchlist.add(listing)
        return HttpResponseRedirect(reverse("index"))
    
def unwatch(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["id"])
        User.objects.get(username=request.user).watchlist.remove(listing)
        return HttpResponseRedirect(reverse("index"))
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })

def category(request, name):
    category = Category.objects.filter(name=name).first()
    listings = Listing.objects.filter(category=category).all()
    return render(request, "auctions/category.html", {
        "name": category.name,
        "listings": listings,
    })

def comment(request, id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            list = Listing.objects.get(pk=id)
            text = form.cleaned_data["text"]

            comment = Comment(poster=request.user,
                              text=text,
                              listing=list)
            
            comment.save()

            # redirect to listing
            return HttpResponseRedirect(reverse("listing", args=[list.id]))
