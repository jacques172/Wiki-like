from django.shortcuts import render, redirect
import markdown2
from django.http import HttpResponse
from . import util
from django import forms
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label = "Title", widget = forms.TextInput(attrs={
        "placeholder": "Enter a title", "id": "entry-title"
    }))
    content = forms.CharField(label = "Content\n", widget=forms.Textarea(attrs={
        "id": "entry-content"
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    ef_content = util.get_entry(title)
    if ef_content:
        ef_content_html =markdown2.markdown(ef_content)  
    else:
        return  render(request, "encyclopedia/404.html",{
            "message": "No entry found"
        })    
    context = {
        "title": title,
        "content": ef_content_html
    }
    return render(request, "encyclopedia/entry.html", context)

def search(request):

    keyword = request.GET['keyword']
    if keyword in util.list_entries():
        return redirect('entry_page', title=keyword)
    else:
        recommendation = []
        entries = util.list_entries()
        for entry in entries:
            if keyword.lower() in entry.lower():
                recommendation.append(entry)
        return render(request, "encyclopedia/search.html",{
            "recommendation": recommendation
        })        



def new_page(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html',{
            "form": NewPageForm()
        })
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/404.html", {
                "message": "Entry already exists"
            })
        else:
            util.save_entry(title, content)
            new_markdown = util.get_entry(title)
            html_content = markdown2.markdown(new_markdown)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content,
                "form": NewPageForm()
            }) 


def edit(request, title):
    if util.get_entry(title):
        content = util.get_entry(title)
        if request.method == "POST":
            new_content = request.POST.get('content')
            util.save_entry(title, new_content)
            return redirect('entry_page', title = title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })    
    else:
        return render(request, "encyclopedia/404.html",{
            "message": "This content does not exist"
        })
def rand(request):
    all = util.list_entries()
    rand_entry = random.choice(all)
    md_content = util.get_entry(rand_entry)
    html_content = markdown2.markdown(md_content)
    return render(request, "encyclopedia/entry.html",{
        "title": rand_entry,
        "content": html_content
    })