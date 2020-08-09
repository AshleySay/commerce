from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from decimal import Decimal

from .models import User, Listing, Bids, Comments1, Watchlist
from .forms import NewListingForm, NewBidForm, CommentForm


# Render the template and pass in the listings model as context.
def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
    })

def categories(request):
    categories = set(Listing.objects.all().values_list("category", flat=True))
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    categorylist = Listing.objects.all().filter(category=category)
    return render(request, "auctions/category/category.html", {
        "categorylist": categorylist
    })

def watchlist(request):
    watchlist = list(Watchlist.objects.all().filter(user=request.user.username).values_list('listing', flat=True))
    listing = Listing.objects.all()
    return render(request, "auctions/watchlist/watchlist.html",{
        "listing": listing,
        "watchlist": watchlist
    })

def newlisting(request):
    if request.method == "POST":
        listing = Listing(
            title=request.POST["title"],
            description=request.POST["description"],
            starting_bid=request.POST["starting_bid"],
            image=request.POST["image"],
            category=request.POST["category"],
            user_id=request.user.id)
        listing.save()
    return render(request, "auctions/newlisting.html",{
        "NewListingForm": NewListingForm()
    })

def closelisting(request, title):
    listing = Listing.objects.get(title=title)
    if (listing.is_active == True):
        listing.is_active = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))

def listing(request, title):
    max_bid = Bids.objects.all().filter(bid=Listing.objects.get(title=title)).aggregate(Max("value"))
    
    try:
        temp = Bids.objects.all().filter(value=max_bid["value__max"]).values_list("user")
        top_bidder = temp[0][0]
    except:
        top_bidder = 0

    try:
        watch_check = Watchlist.objects.get(listing=title)
        is_watched = True
    except:
        is_watched = False

    if request.method == "POST":
        if "SubmitBid" in request.POST:
            bid = Bids(
                value=request.POST["bid"],
                bid=Listing.objects.get(title=title),
                user_id=request.user.id
            )
            if (float(bid.value) > Listing.objects.get(title=title).starting_bid):
                if not max_bid["value__max"] or (float(bid.value) > max_bid["value__max"]):
                    bid.save()
            else:
                return HttpResponse("Invalid Bid. Either less than original or less than largest")
        elif "SubmitComment" in request.POST:
            comment = Comments1(
                content=request.POST["content"],
                item=Listing.objects.get(title=title),
                user_id=request.user.id,
                username=request.user.username
                )
            comment.save()
        elif "AddWatchlist" in request.POST:
            watchitem = Watchlist(
                item =Listing.objects.get(title=title),
                user=request.user.username,
                listing=title
            )
            watchitem.save()
            is_watched = True
    return render(request, "auctions/listing.html",{
        "listing": Listing.objects.get(title=title),
        "bids": Bids.objects.all().filter(bid=Listing.objects.get(title=title)),
        "NewBidForm": NewBidForm(),
        "CommentForm": CommentForm(),
        "top_bidder": top_bidder,
        "comments": Comments1.objects.all().filter(item=Listing.objects.get(title=title)),
        "is_watched": is_watched,
        "max_bid": max_bid["value__max"]
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
