from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>/", views.listing, name="listing"),
    path("<str:category>/", views.categorypage, name="categorypage"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("bid_up", views.bid_up, name="bid_up"),
    path("categories", views.categories, name="categories"),
    path("watchpage", views.watchpage, name="watchpage"),
    path("listing_operations", views.listing_operations, name="listing_operations"),
]
