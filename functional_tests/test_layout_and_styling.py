from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # User goes to the homepage
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # User sees a nicely centered input box
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2,
                               512, delta=6)
