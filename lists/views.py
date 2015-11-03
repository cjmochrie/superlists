from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, ToDoList


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    return render(request, 'list.html', {'todo_list': todo_list})


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

    return redirect('/lists/{}/'.format(list_.id))

def add_item(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
    return redirect('/lists/{}/'.format(todo_list.id))
