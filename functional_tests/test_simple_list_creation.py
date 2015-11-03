from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Check out the app on its homepage
        self.browser.get(self.server_url)

        # The reader notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do item immediately
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # User types 'buy peacock feathers' into a text box
        inputbox.send_keys('buy peacock feathers')

        # After hitting enter, the page updates and now the page lists
        # "1. buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: buy peacock feathers')

        # User can add another item to the to-do list
        inputbox = self.get_item_input_box()
        inputbox.send_keys('use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: buy peacock feathers')
        self.check_for_row_in_list_table('2: use peacock feathers to make a fly')

        # Now a new user, Francis

        # Use a new browser session to make sure that no information is coming along
        self.browser.quit()
        self.browser = webdriver.Chrome('C:\Program Files\chromedriver\chromedriver')

        # Francis visits the home page. No sign of Edith's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy peacock feathers', page_text)
        self.assertNotIn('use peacock feathers to make a fly', page_text)

        # Francis starts a new List by entering a new item
        inputbox = self.get_item_input_box()
        inputbox.send_keys('buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # No trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy peacock feathers', page_text)
        self.assertNotIn('use peacock feathers to make a fly', page_text)

        self.fail('Finish the test!')