from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Max

from .models import User, Profile, Category, Listings, Bids, Watchlist, Items, Comments


def index(request):
    list = Items.objects.all()
    return render(request, "auctions/index.html", {
        "items": list,
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
        return render(request, "auctions/createprofile.html", {
            "message": username,
        })
    else:
        return render(request, "auctions/register.html")

@login_required
def create_Profile(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        phone = request.POST["phone"]

        profile = Profile(user=user,first_name=first_name, last_name=last_name, phone=phone)
        profile.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/createprofile.html')
    
@login_required
def additem(request):
    category = Category.objects.all()
    return render(request, "auctions/additem.html", {
        "cat": category,
    })


@login_required
def add(request):
    if request.method == "POST":
        
        data=request.POST
        cat = Category.objects.get(name=request.POST.get('category'))
        name = data.get('product_name')
        description = data.get('product_discription')
        price = data.get('starting_price')
        image = request.FILES.get('product_img')
        created_by = request.user

        Listings.objects.create(
            category = cat,
            name = name,
            description = description,
            price = price,
            image = image,
            created_by = created_by,
        )

        Items.objects.create(
            category = cat,
            name = name,
            description = description,
            price = price,
            image = image,
            created_by = created_by,
        )

        Bids.objects.create(
            product = name,
            bidder = created_by,
            bids =  price,
        )



        return HttpResponseRedirect(reverse('index'))
    
    list = Listings.objects.all()
    
    return render(request, 'auctions/index.html', {
            "data": list,
    })

@login_required
def details(request, id):
    detail = Items.objects.get(id=id)
    item = Bids.objects.get(product=detail.name)
    product = Items.objects.get(name=detail.name)
    user = request.user
    a = Bids.objects.filter(product=detail.name)
    w = a.order_by('-bids').first()
    print(w.bidder)
    check = False
    box = False
    b = False
    h = detail.sold_to
    print(h)

    if request.GET.get('bid'):
        bid = request.GET.get('bid')
        c = float(bid)
        
        if detail.price <= c and item.bids <= c:
            item.bids = c
            item.bidder = user
            item.save() 
            return HttpResponseRedirect(reverse('detail', args=(id,)))
        else:
            m = 'Your bid is low'
            return render(request, 'auctions/itemdetails.html', {
                "item": detail,
                "bid": item,
                "message": m,
            })
        
    if Watchlist.objects.filter(User=user, products=detail).exists():
        check = True

    
    if detail.is_sold == True:
        b = True
        msg = "Bidding is off and sold to %s" % detail.sold_to
    
    else: 
        msg = "Bidding is on!!!!"


    if detail.created_by == request.user and detail.is_sold == False:
        box = True
        send = "You have not sold this item"

        if request.method == "GET":
            c = request.GET.get('radio')
            print(c)

            if c == "YES":
                detail.is_sold = True
                detail.sold_to = w.bidder
                product.is_sold = True
                product.sold_to = w.bidder
                product.save() 
                detail.save()
                send = "Item sold"
            else:
                send = "You have not sold this item"

    else:
        send = "Bid at your price"

    
    if detail.is_sold == True:
        send = "Item sold"
    
    if request.method == "POST":
        e = request.POST.get('comment')
        
        Comments.objects.create(
            User= request.user,
            product=detail,
            Comment=e,
        )

        return HttpResponseRedirect(reverse('detail', args=(id,)))

    comment = Comments.objects.filter(product=detail)

    return render(request, 'auctions/itemdetails.html', {
        "item": detail,
        "bid": item,
        "u": user,
        "check": check,
        "high": w,
        "box": box,
        "send": send,
        "msg": msg,
        "b": b,
        "h":h,
        "comments": comment,
    })

def watchlist(request):
    user = request.user
    items = Watchlist.objects.all()
    useritem = items.filter(User=user)
    return render(request, 'auctions/watchlist.html', {
        "item": useritem,
    })

def add_to_watchlist(request, id):
    user = request.user
    item = Items.objects.get(id=id)

    Watchlist.objects.create(
        User = user,
        products = item,
    )

    return HttpResponseRedirect(reverse('detail', args=(id,)))

def delete(request, id):
    user = request.user
    item = Items.objects.get(id=id)

    d = Watchlist.objects.filter(User=user, products=item)
    d.delete()

    return HttpResponseRedirect(reverse('detail', args=(id,)))

def profile(request):
    e = request.user
    u = User.objects.get(username=request.user.username)
    banda = Profile.objects.filter(user=e)
    print(u)
    print(e)
    print(banda)

    return render(request, 'auctions/profile.html', {
        "banda": banda,
        "u": u,
    })


def edit_profile(request):
    e = request.user
    u = User.objects.get(username=request.user.username)
    banda = Profile.objects.get(user=e)
    print(u)
    print(e)
    print(banda)

    if request.method == "POST":
        
        data = request.POST
        phone = data.get('phone')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if phone:
            banda.phone = phone
        if first_name:
            banda.first_name = first_name
        if last_name:
            banda.last_name = last_name

        banda.save()

        return HttpResponseRedirect('myprofile')

    return render(request, 'auctions/editprofile.html', {
        "person":banda,
        "u":u,
    })

def mylistings(request):
    user = request.user
    list = Items.objects.filter(created_by=user)
    return render(request, "auctions/mylistings.html", {
        "items": list,
    })

def allproduct(request):
    cat = Category.objects.all()
    list = Items.objects.all()
    if request.GET.get('search_product'):
        f = request.GET.get('search_product')
        list = Items.objects.filter(category__name=request.GET.get('search_product'))

    print('search_product')
      
    return render(request, 'auctions/allproduct.html', {
        "items": list,
        "cat": cat,
    })

def mybuy(request):
    user = request.user
    list = Items.objects.filter(sold_to=user)
    return render(request, "auctions/mylistings.html", {
        "items": list,
    })

def show_watched(request, id):
    w = Watchlist.objects.get(id=id)
    p = Items.objects.get(name=w.products.name)
    print(w.id)
    print(p.id)
    return HttpResponseRedirect(reverse('detail', args=(p.id,)))


def add_comment(request, id):
    detail = Items.objects.get(id=id)
    if request.method == "GET":
        e = request.GET.get('comment')
        
        fresh = Comments(User=request.user, product=detail, Comment= e)
        print(fresh)

        return HttpResponseRedirect(reverse('detail', args=(id,)))