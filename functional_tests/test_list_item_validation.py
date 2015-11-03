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
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # User tries again, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # The user submits a second blank list item
        self.get_item_input_box().send_keys('\n')

        # A similar warning appears
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # The user can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
