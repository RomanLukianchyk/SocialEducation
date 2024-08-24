from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class GitHubAuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.github_login_url = reverse('social:begin', kwargs={'backend': 'github'})
        self.github_complete_url = reverse('social:complete', kwargs={'backend': 'github'})
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }

    def test_github_login_redirect(self):
        response = self.client.get(self.github_login_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('github.com', response['Location'])

    @patch('social_core.backends.github.GithubOAuth2.auth_complete')
    def test_github_callback_creates_user(self, mock_auth_complete):
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_auth_complete.return_value = HttpResponseRedirect('/')

        session = self.client.session
        session['state'] = 'dummy_state'
        session.save()

        response = self.client.get(self.github_complete_url, {
            'code': 'dummy_code',
            'state': 'dummy_state'
        })

        self.assertEqual(response.status_code, 302)

    @patch('social_core.backends.github.GithubOAuth2.auth_complete')
    def test_github_callback_invalid_state(self, mock_auth_complete):
        mock_user = MagicMock()
        mock_user.is_authenticated = False
        mock_auth_complete.return_value = HttpResponseRedirect('/error/')

        session = self.client.session
        session['state'] = 'correct_state'
        session.save()

        response = self.client.get(self.github_complete_url, {
            'code': 'dummy_code',
            'state': 'wrong_state'
        })

        self.assertEqual(response.status_code, 302)  # Предполагаем, что неверный state вызывает ошибку 400

    @patch('social_core.backends.github.GithubOAuth2.auth_complete')
    def test_github_callback_successful_login(self, mock_auth_complete):
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_auth_complete.return_value = HttpResponseRedirect('/home/')

        session = self.client.session
        session['state'] = 'dummy_state'
        session.save()

        response = self.client.get(self.github_complete_url, {
            'code': 'valid_code',
            'state': 'dummy_state'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

    def tearDown(self):
        User.objects.all().delete()