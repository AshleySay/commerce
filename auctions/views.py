from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Listing, Bids


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
    })

def newlisting(request):
    if request.method == "POST":
        listing = Listing(
            title=request.POST["title"],
            description=request.POST["description"],
            starting_bid=request.POST["starting_bid"],
            image=request.POST["image"],
            category=request.POST["category"])
        listing.save()
    return render(request, "auctions/newlisting.html")

def listing(request, title):
    listing = Listing.objects.get(title=title)
    max_bid = Bids.objects.all().filter(bid=Listing.objects.get(title=title)).aggregate(Max("value"))
    if request.method == "POST":
        bid = Bids(
            value=request.POST["bid"],
            bid=Listing.objects.get(title=title)
        )
        if (float(bid.value) > listing.starting_bid) and (float(bid.value) > max_bid["value__max"]):
            bid.save()
        else:
            return HttpResponse("Invalid Bid. Either less then original or less then largest")
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "bids": Bids.objects.all().filter(bid=Listing.objects.get(title=title)),
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
