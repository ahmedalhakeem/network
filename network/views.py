from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.forms import forms
from django.core.paginator import Paginator
import datetime
from django.utils import timezone


from .models import User, Post
from .forms import *


def index(request):

    #display all posts 
    allposts = Post.objects.all().order_by('-timestamp')
    paginator =  Paginator(allposts, 10) 
    page_number = request.GET.get('page')
    allposts = paginator.get_page(page_number)
    #user = User.objects.get(pk = request.user.id)
    #print(user)
    new_post = PostForm()
    return render(request, "network/index.html",{
        "new_post" : new_post,
        "allposts" : allposts,
        
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
    form = PostForm(request.POST or None, request.FILES or None)
    poster = User.objects.get(pk= request.user.id)

    if form.is_valid():
        content = form.cleaned_data['content']
        image = form.cleaned_data['image']
        new_post = Post(content=content,timestamp=datetime.datetime.now(), created_by=poster, image=image)
        print(new_post.timestamp)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))

@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)

    user_login= User.objects.get(pk=request.user.id)

    if(request.user.id == user.id):
        follow=False
    else:
        follow = True
    is_follow = user.following.filter(username=user_login).exists()
    followers = user.following.all().count()
    following = user.followers.all().count()
    allposts = Post.objects.filter(created_by=user_id).order_by('-timestamp')
    
    

    return render(request, "network/profile.html",{
        "following": following,
        "followers": followers,
        "allposts" : allposts,
        "follow" : follow,
        "user_id" : user_id,
        "is_follow" : is_follow
    })

@login_required
def following(request, user_id):
    user = User.objects.get(pk=user_id)
    followings = user.followers.all()
    posts = Post.objects.filter(created_by__in=followings).order_by('-timestamp')
    print(followings)
    for following in followings:
        poster = Post.objects.filter(created_by=following)
        print(poster)
        
    
    #for follow in followings:
     #   f = Post.objects.filter(created_by=follow)
      #  print(f)

    return render(request, "network/following.html",{
        #"poster" : poster,
        "posts" : posts
        
    })

def editpost(request, post_id):
    post = Post.objects.get(pk=post_id)
    newpost = request.GET["newpost"]
    post.content=newpost
    post.timestamp = datetime.datetime.now()
    post.save()
    return JsonResponse({"status": "success"}) 
        
def follow(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    follower = User.objects.get(pk=request.user.id)
    if profile_user.following.filter(username=follower).exists():
        profile_user.following.remove(follower) 
    else:
        profile_user.following.add(follower)
   # print(profile_user)
    #print(follower)
    return HttpResponseRedirect(reverse('profile',args=(user_id,)))

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.like.filter(username= request.user).exists():
        post.like.remove(request.user)
        post.num_likes= post.like.all().count()
        

    else:
        post.like.add(request.user)
        post.num_likes = post.like.all().count()
        
    post.save()
    return JsonResponse({"status": "success", "num_likes": post.like.all().count() })

def check_like(request):
    post = Post.objects.get(pk=request.GET["id"])
    return JsonResponse({
        'isLike': post.like.filter(username=request.user).exists()
    })
    