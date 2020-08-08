from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("category/category/<str:category>", views.category, name="category/category"),
    path("<str:title>", views.listing, name="listing"),
    path("closelisting/<str:title>", views.closelisting, name="closelisting"),
    path("watchlist/watchlist", views.watchlist, name="watchlist/watchlist")
]
