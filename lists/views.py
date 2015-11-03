from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, ToDoList
from .forms import ItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], todo_list=todo_list)
            return redirect(todo_list)

    return render(request, 'list.html', {'todo_list': todo_list, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = ToDoList.objects.create()
        item = Item.objects.create(text=request.POST['text'], todo_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})
