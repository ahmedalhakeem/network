from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import forms

from .models import User
from .forms import *



def index(request):

    #display all posts 
    allposts = Post.objects.all().order_by('-timestamp')
    
    if request.method == 'POST':
         new_post = PostForm(request.POST)
         if new_post.is_valid():
             content = new_post.cleaned_data['content']
             #timestamp = new_post.cleaned_data['timestamp']
             #created_by = new_post.cleaned_data['created_by']
             return HttpResponseRedirect(reverse('post'))
             
    else:
        new_post = PostForm()
        return render(request, "network/index.html",{
            "new_post" : new_post,
            "allposts" : allposts
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def post(request):
    poster = User.objects.get(pk= request.user.id)

    if request.method == "POST":
        content = request.POST['content']
        new_post = Post(content=content, created_by=poster)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))

def profile(user_id):
    return