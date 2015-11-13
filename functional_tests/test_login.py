import time
from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest

TEST_EMAIL ='cameron@mockmyid.com'

class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # User sees login link on home page and clicks it
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # The user logs in with her email address
        ## Use mockmyid.com for test email
        self.browser.find_element_by_id('authentication_email').\
            send_keys(TEST_EMAIL)
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # User can see he is logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # After refreshing the page the user still sees he is logged in
        self.browser.refresh()
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # The user logs out
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

        # Logged out status persists
        self.browser.refresh()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

    def switch_to_new_window(self, text_in_title):
        for i in range(60):
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    time.sleep(.5)
                    return
            time.sleep(0.3)
        self.fail('could not find window')

