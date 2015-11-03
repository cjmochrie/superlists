from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, ToDoList


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
            item.full_clean()
            item.save()
            return redirect(todo_list)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'todo_list': todo_list, 'error': error})


def new_list(request):
    list_ = ToDoList.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], todo_list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(request, 'home.html',
                      {'error': "You can't have an empty list item"})

    return redirect(list_)
