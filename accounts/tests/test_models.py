from django.core.files.storage import default_storage
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import Profile
import io
from PIL import Image


class AccountsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='rlukianchyk@gmail.com', password='password123')

    @staticmethod
    def create_test_image():
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'JPEG')
        file.name = 'test_image.jpg'
        file.seek(0)
        return file

    def test_profile_creation(self):
        profile, created = Profile.objects.get_or_create(user=self.user,
                                                         defaults={'full_name': 'tester', 'bio': 'Test bio'})
        self.assertTrue(created, msg="Profile should be created.")
        self.assertEqual(profile.user.username, 'tester')
        self.assertEqual(profile.full_name, 'tester')
        self.assertEqual(profile.bio, 'Test bio')
        self.assertIsNotNone(profile.avatar, msg="Avatar field should be created.")

    def test_profile_str_method(self):
        profile, created = Profile.objects.get_or_create(user=self.user, defaults={'full_name': 'tester'})
        self.assertTrue(created, msg="Profile should be created.")
        self.assertEqual(str(profile), 'tester')

    def test_profile_avatar_upload(self):
        avatar = SimpleUploadedFile(name='avatar.jpg', content=self.create_test_image().read(),
                                    content_type='image/jpeg')
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.avatar = avatar
        profile.save()
        self.assertIsNotNone(profile.avatar)
        self.assertTrue(default_storage.exists(profile.avatar.name))
        self.assertIn('avatar', profile.avatar.name)

    def test_profile_avatar_blank(self):
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertTrue(created, msg="Profile should be created.")
        self.assertFalse(profile.avatar, msg="Avatar should be blank by default.")

    def test_profile_creation_without_full_name_and_bio(self):
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertTrue(created, msg="Profile should be created.")
        self.assertEqual(profile.full_name, '')
        self.assertEqual(profile.bio, '')

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
