from django.shortcuts import render, redirect
from .models import Item, ToDoList


def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    list_ = ToDoList.objects.create()
    items = Item.objects.create(text=request.POST['item_text'], todo_list=list_)
    return redirect('/lists/the-only-list-in-the-world/')