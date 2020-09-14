from django.urls import path

from . import views

urlpatterns = [
    path("", views.index1, name="index1"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:q>", views.search, name="search"),
    path("wiki/edit/", views.edit, name="edit"),
    path("wiki/update/", views.update, name="update"),
    path("wiki/createPage/", views.createPage, name="createPage"),
    path("wiki/random/", views.randomPage, name="randomPage")
]
