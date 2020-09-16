from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2
import random


# This is a new render function
class searchForm(forms.Form):
    q = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Search Encyclopedia'
    }))


# This create a form object
class newPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Enter your Title here'
                            }))
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your MD text here'
        }
        ))


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
        if "pageCreated" not in request.session:
            request.session['pageCreated'] = False
        elif request.session.get('pageCreated') == True:
            pageCreated = True
            request.session['pageCreated'] = False
        else:
            pageCreated = False
        return render(request, "encyclopedia/index.html", {
            "pageCreated": pageCreated,
            "newPage": request.session["newpage"],
            "searchForm": searchForm(),
            "entries": util.list_entries()
        })


# This gives list of suggested seraches
def suggest(request, q):
    s = []
    for i in util.list_entries():
        if q.casefold() in i.casefold():
            s.append(i)
    return s


# This is the search result page of the website
def search(request, q=None):
    if q and q != '':
        content = util.get_entry(q)
        s = suggest(request, q)
        if content:
            return render(request, "encyclopedia/search.html", {
                "searchForm": searchForm(),
                "title": q,
                "content": markdown2.markdown(content)
            })
        elif s:
            return render(request, "encyclopedia/suggestions.html", {
                "searchForm": searchForm(),
                "q": q,
                "nResult": len(s),
                "entries": s
            })
        else:
            return render(request, "encyclopedia/404.html", {
                "searchForm": searchForm(),
            })
    else:
        return HttpResponseRedirect(reverse("index"))


# This render to the existing page
def edit(request, method=["POST"]):
    t = request.POST["title"]
    form = newPageForm(initial={
        "title": t,
        "content": util.get_entry(t)
    })
    return render(request, "encyclopedia/edit.html", {
        "searchForm": searchForm(),
        "title": t,
        "form": form
    })


# This updates the server data
def update(request, method=["POST"]):
    return createPage(request, update=True)


# This Creates a new wiki Page
def createPage(request, methods=["GET", "POST"], update=False):
    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title) or update:
                util.save_entry(title, content)
                request.session["pageCreated"] = True
                request.session["newpage"] = title
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
