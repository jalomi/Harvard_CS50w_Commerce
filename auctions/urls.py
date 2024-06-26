from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.new_listing, name="add"),
    path('listing/<int:id>', views.listing, name="listing"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('watch', views.watch, name="watch"),
    path('unwatch', views.unwatch, name="unwatch"),
    path('categories', views.categories, name="categories"),
    path('category/<str:name>', views.category, name="category"),
]
