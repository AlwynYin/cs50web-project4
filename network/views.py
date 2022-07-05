import json
from tkinter import W
from turtle import pos
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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


# apis
@login_required
def new_post(request):
    '''
    creates a new post\n
    request body should be in this way\n
    {\n
        "content": content\n
    }
    '''
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    try:
        body = json.loads(request.body)
        if body["content"] == "":
            return JsonResponse({"status": "fail", "error": "content cannot be blank"})
        post = Post.objects.create(sender=request.user, content=body["content"])
        post.save()
        return JsonResponse({"status": "success"}, status=200)
    except:
        return JsonResponse({"status": "fail"}, status=502)


@login_required
def user_posts(request):
    raise NotImplementedError


@login_required
def all_posts(request):
    '''
    return a list of all not deleted post
    '''
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)
    
    try:
        response = {"status": "success"}
        all_posts = Post.objects.all()
        response["posts"] = [{"sender": post.sender.username, "content": post.content} for post in all_posts]
        return JsonResponse(response)
    except:
        return JsonResponse({"status": "fail"}, status=502)