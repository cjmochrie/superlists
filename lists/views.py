from django.shortcuts import render, redirect
from .models import Item, ToDoList


def home_page(request):
    return render(request, 'home.html')



def view_list(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    return render(request, 'list.html', {'todo_list': todo_list})


def new_list(request):

    list_ = ToDoList.objects.create()
    Item.objects.create(text=request.POST['item_text'], todo_list=list_)
    return redirect('/lists/{}/'.format(list_.id))

def add_item(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
    return redirect('/lists/{}/'.format(todo_list.id))
