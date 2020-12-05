
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<user_id>", views.profile, name="profile"),
    path("following/<user_id>", views.following, name="following"),
    path("editpost/<int:post_id>", views.editpost, name = "editpost"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path('check_like', views.check_like, name = 'check_like')

]
