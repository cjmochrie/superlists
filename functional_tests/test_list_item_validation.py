from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):


    def test_cannot_add_empty_list_items(self):
        # User goes to the homepage and submits an empty list item.

        # The homepage refreshes and an error message appears saying that list items
        # cannot be blank

        # User tries again, which now works

        # The user submits a second blank list item

        # A similar warning appears

        # The user can correct it by filling some text in
        self.fail('Not implemented')
