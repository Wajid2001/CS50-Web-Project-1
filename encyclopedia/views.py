from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2


# If the User vist direct website not "wiki/"
def index1(request):
    return HttpResponseRedirect(reverse("index"))


# This is the Main Page of the website
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# This is the search result page of the website
def search(request, q):
    if q and q != '':
        content = util.get_entry(q)
        if content:
            return render(request, "encyclopedia/search.html", {
                "content": markdown2.markdown(content)
            })
        else:
            return render(request, "encyclopedia/404.html")
    else:
        return HttpResponseRedirect(reverse("index"))
