from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .form import create_form, bid_form, new_comment
from .models import User, Listing, Bid, Watch, Comment
from django.db.models import Max, F
from .utils import highest_bid, face_blurr


def listing_operations(request):
    if request.method == "POST":
        if 'listing' in request.POST:
            # close listing
            listing_id = request.POST["listing"]
            username = request.user.username
            user=User.objects.get(username=username)
            try:
                check_listing = Listing.objects.get(id=listing_id, owner=user)
            except:
                check_listing = None
            if check_listing:
                x = Listing.objects.get(id=listing_id, owner=user)
                x.status = False
                x.save()
            html = "<a href= %s > <h2>Well done, click to back </h2> </a>" % listing_id
            return HttpResponse(html)

        elif 'text' in request.POST :
            # add comment
            text = request.POST['text']
            listing_id = request.POST['listing_id']
            print(listing_id)
            listing = Listing.objects.get(id=listing_id)
            username = request.user.username
            user=User.objects.get(username=username)
            print(type(listing))
            Comment.objects.create(listing_id=listing, user_id=user,text=text)
            html = "<a href= %s > <h2>Well done, click to back </h2> </a>" % listing_id
            return redirect('/'+ str(listing.id))

    return HttpResponse("Problem")

def bid_up(request):
    # function for bid up listings
    form = bid_form()
    if request.method=="POST":
        username = request.user.username
        user=User.objects.get(username=username)
        bid_up = request.POST["bid_up"]
        listing_id = request.POST["listing_id"]
        bid_h = highest_bid(listing_id)
        listing = Listing.objects.get(id=listing_id)

        if float(bid_h.price) < float(bid_up):
            Bid.objects.create(listing_id=listing, user_id=user, price=bid_up)
            html = "<a href= %s > <h2>Well done, click to back </h2> </a>" % listing_id
            return redirect('/'+ str(listing.id))
        else:
            html = "<a href= %s > <h2>Your bid it's too small, click to back </h2> </a>" % listing_id
            return HttpResponse(html)
    else:
        return HttpResponse("nie dziala")

def listing(request, listing_id):
    # biggest bet from all listings
    b = Bid.objects.annotate(
    highest=Max('listing_id__listing__price')
).filter(
    price=F('highest'))
    listing = Listing.objects.get(id=listing_id)
    # getting our listing highest bet
    form = bid_form()
    form_comment = new_comment()
    for i in b:
        if i.listing_id == listing:
            b = i
    # Check are listing are on user watchlist
    on_watchlist = False

    try:
        username = request.user.username
        user=User.objects.get(username=username)
        on_watchlist = Watch.objects.get(user=user, auction=listing)
    except:
        on_watchlist = False

    # Get comments ordered in order
    comments = Comment.objects.filter(listing_id=listing)
    

    return render(request, "auctions/listing.html", {
        "listing_id":listing_id,
        "listing":Listing.objects.get(id=listing_id),
        "bid":b,
        "form":form,
        "on_watchlist":on_watchlist,
        "comments":comments,
        "new_comment":form_comment,

            
    })

def categorypage(request, category):
    # display categories
    listings = Listing.objects.filter(category=category)
    print(category)
    b = Bid.objects.annotate(
    highest=Max('listing_id__listing__price')
).filter(
    price=F('highest'))

    return render(request, "auctions/categorypage.html",{
        "listings":listings,
        "bid":b,
        "category":category
    })
    pass

def add_watchlist(request):
    # button "add listing to watchlist"
    if request.method == "POST":
        listing_id = request.POST["listing"]
        username = request.user.username
        user=User.objects.get(username=username)
        listing = Listing.objects.get(id=listing_id)
        try:
            check_listing = Watch.objects.get(user=user, auction=listing)
        except:
            check_listing = None
        if not check_listing:
            new = Watch.objects.create(user=user, auction=listing)
        html = "<a href= %s > <h2>Well done, click to back </h2> </a>" % listing_id
        return redirect('/'+ str(listing.id))


def remove_watchlist(request):
    # button "remove listing to watchlist"
    if request.method == "POST":
        listing_id = request.POST["listing"]
        username = request.user.username
        user=User.objects.get(username=username)
        listing = Listing.objects.get(id=listing_id)
        try:
            check_listing = Watch.objects.get(user=user, auction=listing)
        except:
            check_listing = None
        if check_listing:
            Watch.objects.get(user=user, auction=listing).delete()
        html = "<a href= %s > <h2>Well done, click to back </h2> </a>" % listing_id
        return redirect('/'+ str(listing.id))

def categories(request):
    categories = Listing.objects.values('category').distinct()

    return render(request, "auctions/categories.html",{
    "categories":categories,
    })



def index(request):
    b = Bid.objects.annotate(
    highest=Max('listing_id__listing__price')
).filter(
    price=F('highest'))

    return render(request, "auctions/index.html",{
        "listing":Listing.objects.all(),
        "bid":b
    })

def watchpage(request):
    b = Bid.objects.annotate(
    highest=Max('listing_id__listing__price')
).filter(
    price=F('highest'))
    username = request.user.username
    user=User.objects.get(username=username)
    listings = []
    for i in Watch.objects.filter(user=user):
        listings.append(i.auction)
    return render(request, "auctions/watchpage.html",{
        "listings":listings,
        "bid":b
    })

def create(request):
    if request.method == "POST":
        form = create_form(request.POST, request.FILES)
        if form.is_valid():
            # Get date from form
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            start_bid = form.cleaned_data['start_bid']
            category = form.cleaned_data['category']
            img = request.FILES['img']
            # find   user
            username = request.user.username
            user=User.objects.get(username=username)
            # Add new listing to db
            add_listing = Listing.objects.create(title=title, description=text, category=category, owner=user, img=img)
            img = Listing.objects.get(id=add_listing.id)
            img = face_blurr(img.img)
            # add bid
            add_bid = Bid.objects.create(listing_id =add_listing ,user_id=user ,price=start_bid)

            # out of a view context
            return redirect('/'+ str(add_listing.id))
            
    return render(request, "auctions/create.html", {
        "form": create_form()
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
