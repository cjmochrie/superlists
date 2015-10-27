from django.db import models



class ToDoList(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    todo_list = models.ForeignKey(ToDoList, default=None)
