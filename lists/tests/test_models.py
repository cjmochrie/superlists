from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, ToDoList


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):

        list_ = ToDoList()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.todo_list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.todo_list = list_
        second_item.save()

        saved_list = ToDoList.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.todo_list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.todo_list, list_)


    def test_duplicate_items_are_invalid(self):
        list_ = ToDoList.objects.create()
        Item.objects.create(todo_list=list_, text='foo')
        with self.assertRaises(ValidationError):
            item = Item(todo_list=list_, text='foo')
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = ToDoList.objects.create()
        list2 = ToDoList.objects.create()
        Item.objects.create(todo_list=list1, text='fff')
        item = Item(todo_list=list2, text='fff')
        item.full_clean() # should not raise


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = ToDoList.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/{}/'.format(list_.id))


class ListAndItemModelsTest(TestCase):

    def test_cannot_save_empty_list_items(self):
        list_ = ToDoList.objects.create()
        item = Item(todo_list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()