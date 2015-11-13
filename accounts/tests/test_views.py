from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from unittest.mock import patch

User = get_user_model()

class LoginViewTest(TestCase):


    def test_calls_authenticate_with_assertion_from_post(self):
        with patch('accounts.views.authenticate') as mock_authenticate:
            mock_authenticate.return_value = None # configure the mock object
            self.client.post('/accounts/login', {'assertion': 'assert this'})
            mock_authenticate.assert_called_once_with(assertion='assert this')

    def test_returns_OK_when_user_found(self):
        with patch('accounts.views.authenticate') as authenticate:
            user = User.objects.create(email='a@b.com')
            user.backend = '' # required for auth_login to work
            authenticate.return_value = user
            response = self.client.post('/accounts/login', {'assertion': 'a'})
            self.assertEqual(response.content.decode(), 'OK')

    def test_gets_logged_in_session_if_authenticate_returns_a_user(self):
        with patch('accounts.views.authenticate') as authenticate:
            user = User.objects.create(email='a@b.com')
            user.backend = ''
            authenticate.return_value = user
            self.client.post('/accounts/login', {'assertion': 'a'})
            self.assertEqual(self.client.session[SESSION_KEY], str(user.pk)) # pk = primary key

    @patch('accounts.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_None(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertNotIn(SESSION_KEY, self.client.session)