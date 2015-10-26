import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('C:\Program Files\chromedriver\chromedriver')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Check out the app on its homepage
        self.browser.get('http://localhost:8000')

        # The reader notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the Test!')

        # Bunch more narrative


if __name__ == '__main__':
    unittest.main()