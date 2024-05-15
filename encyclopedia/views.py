import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import random
import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'title':'All'
    })

def get_entry_page(request, title):
    #looking for the entry in the list of entries
    the_content = util.get_entry(title)

    #in case the entry dosent exist
    if the_content is None:
        return render(request, 'encyclopedia/error.html', {
            'error': 'The search do not match any existing page... u can create your own page with the Create a new page section button'
        })

    #if it does
    return render(request, "encyclopedia/entry.html", {
        "the_content":''.join(markdown.markdown(the_content)[i] for i in range(len(markdown.markdown(the_content)))),
        "title": title
    })

def search(request):
    #getting the search query
    q = request.GET.get('q')

    #an empty query
    if q == '':
        return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries(),
        'title':'All'
    })

    q_entry = util.get_entry(q)

    #if the query is a substring for an entry
    if q_entry is None:
        entries = util.list_entries()
        
        entry = (entries[i] for i in range(len(entries)) if q.lower() in entries[i].lower())

        if entry == []:
            return render(request, 'encyclopedia/error.html', {
                'error': 'The search do not match any existing page... u can create your own page with the Create a new page section button'
            })

        return render(request, 'encyclopedia/index.html', {
            'entries' : entry,
            'title':'Result'
        })


    #the query matches an entry
    return render(request, 'encyclopedia/index.html', {
        'entries': [q.capitalize()],
        'title': 'Result'
    })

def new_page(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/create.html')

    if request.method == 'POST':
        entry_name = request.POST.get('title')
        entry_content = request.POST.get('textarea')
        entries = util.list_entries()
        
        #in case the entry already exists
        if any(entry_name.lower() == entrie.lower() for entrie in entries):
            return render(request, 'encyclopedia/error.html', {
                'error': 'Title already exists... u can check the edit section'
            })

        #in case the content is empty
        if entry_content == '':
            return render(request, 'encyclopedia/error.html', {
                'error': 'Please enter the Markdown content' 
            })

        #if everything checks
        util.save_entry(entry_name, entry_content)
        return redirect('get_entry_page', title=entry_name)

def random_page(request):
    entries = util.list_entries()
    return redirect('get_entry_page', title=entries[random.randrange(0, len(entries))])