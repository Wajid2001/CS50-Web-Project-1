from django.urls import path

from . import views

urlpatterns = [
    path("", views.index1, name="index1"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:q>", views.search, name="search"),
    path("wiki/random/", views.randomPage, name="randomPage")
]
