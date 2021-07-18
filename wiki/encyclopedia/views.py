from django.http import HttpResponse, Http404

from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
from random import randint
import markdown 

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, TITLE):
    entry = markdown.markdown(util.get_entry(TITLE))
    print(entry)
    if not entry:  
        return render(request, "encyclopedia/error.html", {"message": "You requested page was not found."})
    return render(request, "encyclopedia/entry.html", {
        "entry": entry, 
        "title": TITLE

    })

def search(request):
    title = request.GET["q"]
    entry = util.get_entry(title)
    new_entries = []
    if not entry: 
        entries = util.list_entries()
        for item in entries: 
            if title in item.lower(): 
                new_entries.append(item)
        
        return render(request, "encyclopedia/search_result.html", {
        "entries": new_entries
    })
    return render(request, "encyclopedia/entry.html", {
        "entry": entry, 
        "title": title

    })

def add(request):
    # Check if method is POST
    if request.method == "POST":
        TITLE = request.POST["title"]
        CONTENT = request.POST["content"]
        entry = util.get_entry(TITLE)
        if not entry:
            util.save_entry(TITLE, CONTENT)
        else: 
            return render(request, "encyclopedia/error.html", {"message": "Your encyclopedia entry already exists with the provided title."})  
        

    return render(request, "encyclopedia/add.html")
    
    
def edit(request, TITLE):
    if request.method == "POST":
        CONTENT = request.POST["content"]
        util.save_entry(TITLE, CONTENT)
        return HttpResponseRedirect(reverse("entry", args=(TITLE,))) 
    entry = util.get_entry(TITLE)
    return render(request, "encyclopedia/edit.html", {
        "entry": entry, 
        "title": TITLE

    })


def random(request):
    entries = util.list_entries()
    entries_length = len(entries)
    random_title = entries[randint(0, (entries_length-1))]
    entry = markdown.markdown(util.get_entry(random_title))
    
    return render(request, "encyclopedia/entry.html", {
        "entry": entry, 
         "title": random_title

    })

    # return HttpResponse("Hello, world!")