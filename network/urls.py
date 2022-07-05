
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # api path
    path("api/posts/user/<int:id>/", views.user_posts, name="user_posts"),
    path("api/posts/new/", views.new_post, name="new_post"),
    path("api/posts/all/", views.all_posts, name="all_posts")
]
