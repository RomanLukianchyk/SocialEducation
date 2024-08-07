from django.test import TestCase
from accounts.forms import ProfileForm
from accounts.models import Profile
from django.contrib.auth.models import User


class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='rlukianchyk@gmail.com', password='password123')

    def test_valid_profile_form(self):
        form_data = {'full_name': 'Tester', 'bio': 'Test bio'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_profile_form(self):
        form_data = {'full_name': '', 'bio': 'Test bio'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_save_profile_form(self):
        form_data = {'full_name': 'Tester', 'bio': 'Test bio'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        profile.user = self.user
        profile.save()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().full_name, 'Tester')
