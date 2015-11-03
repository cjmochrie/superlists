from unittest import skip

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, ToDoList
from lists.views import home_page
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR


class HomePageTest(TestCase):
    maxDiff = None

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'form': ItemForm()})
        self.assertMultiLineEqual(response.content.decode(), expected_html)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = ToDoList.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = ToDoList.objects.create()

        Item.objects.create(text='itemy 1', todo_list=correct_list)
        Item.objects.create(text='itemy 2', todo_list=correct_list)

        other_list = ToDoList.objects.create()
        Item.objects.create(text='other list item 1', todo_list=other_list)
        Item.objects.create(text='other list item 2', todo_list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = ToDoList.objects.create()
        correct_list =ToDoList.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['todo_list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = ToDoList.objects.create()
        correct_list =ToDoList.objects.create()

        self.client.post('/lists/{}/'.format(correct_list.id),
                         data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.todo_list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = ToDoList.objects.create()
        correct_list =ToDoList.objects.create()

        response = self.client.post('/lists/{}/'.format(correct_list.id),
                                    data={'text': 'A new item for an existing list'})


        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def post_invalid_input(self):
        todo_list = ToDoList.objects.create()
        return self.client.post('/lists/{}/'.format(todo_list.id),
                                   data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = ToDoList.objects.create()
        item1 = Item.objects.create(todo_list=list1, text='textey')
        response = self.client.post('/lists/{}'.format(list1.id), data={'text': 'textey'})
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_displays_item_form(self):
        list_ = ToDoList.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = ToDoList.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(ToDoList.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
