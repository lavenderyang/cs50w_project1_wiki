from django.http import HttpResponse, Http404

from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, TITLE):
    entry = util.get_entry(TITLE)
    if not entry:  
        return render(request, "encyclopedia/error.html", {"message": "You requested page was not found."})
    return render(request, "encyclopedia/entry.html", {
        "entry": entry, 
        "title": TITLE

    })

