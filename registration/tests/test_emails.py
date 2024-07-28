from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core import mail
from registration.utils import send_confirmation_email


class EmailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', email='rlukianchyk@gmail.com', password='password123')

    def test_send_confirmation_email(self):
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            request = self.client.get('/').wsgi_request
            send_confirmation_email(request, self.user)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Confirm your registration', mail.outbox[0].subject)
        self.assertIn('Please click the following link to confirm your registration', mail.outbox[0].body)
