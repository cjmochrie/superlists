from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, ToDoList

class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ["You can't have an empty list item"])

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.home()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_form_save_handles_saving_to_a_list(self):
        list_ = ToDoList.objects.create()
        form = ItemForm(data={'text': 'foobar'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'foobar')
        self.assertEqual(new_item.todo_list, list_)


    def home(self):
        return self.client.get('/')