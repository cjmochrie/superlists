from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):


    def test_cannot_add_empty_list_items(self):
        # User goes to the homepage and submits an empty list item.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The homepage refreshes and an error message appears saying that list items
        # cannot be blank
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # User tries again, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # The user submits a second blank list item
        self.get_item_input_box().send_keys('\n')

        # A similar warning appears
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # The user can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # User goes to the homepage, starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        # User accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')

        # User sees a helpful error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # User starts a new list that causes a validation error
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # User starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # The error message disappears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')