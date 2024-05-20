from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createprofile", views.create_Profile, name="create_Profile"),
    path("addlisting", views.additem, name="add"),
    path("add", views.add, name="added"),
    path("detail/<id>/", views.details, name="detail"),
    path("watchlist", views.watchlist, name="watch"),
    path("watch/<id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove/<id>", views.delete, name="remove"),
    path("myprofile", views.profile, name="profile"),
    path("editprofile", views.edit_profile, name="edit_profile"),
    path("mylisting", views.mylistings, name="mylisting"),
    path("allproduct", views.allproduct, name="allproduct"),
    path("mybuy", views.mybuy, name="mybuy"),
    path("t/<id>/", views.show_watched, name="t"),
]
