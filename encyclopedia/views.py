from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2
import random


# This is a new render function
class searchForm(forms.Form):
    q = forms.CharField(max_length=100)


# This create a form object
class newPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(
        label="Type Content in MD text", widget=forms.Textarea)


# If the User vist direct website not "wiki/"
def index1(request):
    return HttpResponseRedirect(reverse("index"))


# This is the Main Page of the website
def index(request, methods=["GET", "POST"]):
    if request.method == "POST":
        form = searchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            return search(request, q)
    else:
        return render(request, "encyclopedia/index.html", {
            "searchForm": searchForm(),
            "entries": util.list_entries()
        })


# This is the search result page of the website
def search(request, q=None):
    if q and q != '':
        content = util.get_entry(q)
        if content:
            return render(request, "encyclopedia/search.html", {
                "searchForm": searchForm(),
                "title": q,
                "content": markdown2.markdown(content)
            })
        else:
            return render(request, "encyclopedia/404.html", {
                "searchForm": searchForm(),
            })
    else:
        return HttpResponseRedirect(reverse("index"))


# This Creates a new wiki Page
def createPage(request, methods=["GET", "POST"]):
    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "encyclopedia/createPage.html", {
                    "searchForm": searchForm(),
                    "titleError": True,
                    "form": form
                })
        else:
            return render(request, "encyclopedia/404.html")
    else:
        return render(request, "encyclopedia/createPage.html", {
            "searchForm": searchForm(),
            "titleError": False,
            "form": newPageForm()
        })


# This is render to a random page
def randomPage(request):
    r = random.choice(util.list_entries())
    return search(request, r)
